#!/usr/bin/env python3
'''
ACMG Classifier v0.4.0 - Com Validacao Pydantic
ACMG/AMP 2015 + Validacao de entrada
'''

import csv
import sys
from pathlib import Path
from typing import Dict, List
from pydantic import ValidationError

# Adicionar raiz do projeto ao Python PATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.variants.models import VariantInput


class ACMGCriteria:
    '''Criterios ACMG/AMP 2015 para genes MMR'''
    
    PVS1_GENES = {
        'MLH1': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'MSH2': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'MSH6': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'PMS2': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'EPCAM': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift']
    }
    
    @staticmethod
    def check_pvs1(tipo: str, gene: str) -> bool:
        '''PVS1: Null variant em gene MMR'''
        if gene not in ACMGCriteria.PVS1_GENES:
            return False
        return tipo in ACMGCriteria.PVS1_GENES[gene]
    
    @staticmethod
    def check_ps1(classificacao_original: str) -> bool:
        '''PS1: Ja reportado como Pathogenic'''
        return 'Pathogenic' in classificacao_original and 'Likely' not in classificacao_original
    
    @staticmethod
    def check_pm2(allele_frequency) -> bool:
        '''PM2: Frequencia muito baixa'''
        if not allele_frequency:
            return False
        try:
            freq = float(allele_frequency)
            return freq < 0.00001
        except:
            return False
    
    @staticmethod
    def check_ba1(allele_frequency) -> bool:
        '''BA1: Frequencia alta'''
        if not allele_frequency:
            return False
        try:
            freq = float(allele_frequency)
            return freq > 0.05
        except:
            return False


class ACMGClassifier:
    '''Classifica variantes com ACMG/AMP 2015'''
    
    @staticmethod
    def classificar(variante: Dict) -> Dict:
        '''Classifica variante com validacao Pydantic'''
        
        try:
            variant_validated = VariantInput(**variante)
        except ValidationError as e:
            clinvar = variante.get('clinvar_id', 'DESCONHECIDO')
            msg = e.errors()[0]['msg']
            print(f'ERRO: {clinvar} - {msg}')
            raise
        
        gene = variant_validated.gene
        tipo = variant_validated.tipo
        classificacao_original = variant_validated.classificacao
        allele_frequency = variant_validated.allele_frequency
        
        pathogenic_criteria = []
        benign_criteria = []
        
        if ACMGCriteria.check_pvs1(tipo, gene):
            pathogenic_criteria.append('PVS1')
        
        if ACMGCriteria.check_ps1(classificacao_original):
            pathogenic_criteria.append('PS1')
        
        if ACMGCriteria.check_pm2(allele_frequency):
            pathogenic_criteria.append('PM2')
        
        if ACMGCriteria.check_ba1(allele_frequency):
            benign_criteria.append('BA1')
        
        if 'PVS1' in pathogenic_criteria:
            classification = 'Pathogenic (P)'
            strength = 'Very Strong (PVS1)'
        elif 'PS1' in pathogenic_criteria:
            classification = 'Likely Pathogenic (LP)'
            strength = 'Strong (PS1)'
        elif 'PM2' in pathogenic_criteria:
            classification = 'Likely Pathogenic (LP)'
            strength = 'Moderate (PM2)'
        elif 'BA1' in benign_criteria:
            classification = 'Benign (B)'
            strength = 'Very Strong (BA1)'
        else:
            classification = 'Variant of Uncertain Significance (VUS)'
            strength = 'Insufficient Evidence'
        
        all_criteria = pathogenic_criteria + benign_criteria
        criteria_str = ','.join(all_criteria) if all_criteria else 'None'
        
        variante['acmg_classification'] = classification
        variante['acmg_criteria'] = criteria_str
        variante['acmg_explanation'] = f'{classification} - {strength}'
        
        return variante


def processar_arquivo(input_file: str, output_file: str) -> list:
    '''Processa arquivo com validacao'''
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    print(f'\nLendo: {input_path}')
    
    variantes = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variantes.append(row)
    
    print(f'OK {len(variantes)} variantes lidas')
    print(f'\nValidando e classificando...')
    
    classifier = ACMGClassifier()
    variantes_analisadas = []
    variantes_erro = 0
    
    for var in variantes:
        try:
            var_analisada = classifier.classificar(var)
            variantes_analisadas.append(var_analisada)
            hgvs = var['hgvs']
            gene = var['gene']
            tipo = var['tipo']
            cls = var_analisada['acmg_classification']
            print(f'  {gene}: {hgvs} [{tipo}] -> {cls}')
        except ValidationError:
            variantes_erro += 1
            continue
    
    print(f'\nSalvando: {output_path}')
    if variantes_analisadas:
        fieldnames = list(variantes_analisadas[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(variantes_analisadas)
        
        print(f'OK {len(variantes_analisadas)} variantes processadas!')
        if variantes_erro > 0:
            print(f'AVISO {variantes_erro} variante(s) com erro')
    
    return variantes_analisadas


def main():
    print('\n' + '='*70)
    print('ACMG Classifier v0.4.0 - Com Validacao Pydantic')
    print('='*70)
    
    input_file = 'data/raw/clinvar_mmr_variants.csv'
    output_file = 'data/processed/clinvar_mmr_with_acmg_v0.4.0.csv'
    
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    
    variantes = processar_arquivo(input_file, output_file)
    
    print('\n' + '='*70)
    print('RESUMO v0.4.0 (Com Validacao)')
    print('='*70)
    
    pathogenic = sum(1 for v in variantes if v['acmg_classification'] == 'Pathogenic (P)')
    likely_pathogenic = sum(1 for v in variantes if v['acmg_classification'] == 'Likely Pathogenic (LP)')
    vus = sum(1 for v in variantes if 'VUS' in v['acmg_classification'])
    benign = sum(1 for v in variantes if v['acmg_classification'] == 'Benign (B)')
    
    print(f'\nPathogenic (P): {pathogenic}')
    print(f'Likely Pathogenic (LP): {likely_pathogenic}')
    print(f'VUS: {vus}')
    print(f'Benign (B): {benign}')
    print(f'Total: {len(variantes)} variantes')
    print('='*70 + '\n')


if __name__ == '__main__':
    main()
