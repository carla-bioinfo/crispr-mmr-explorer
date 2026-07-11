#!/usr/bin/env python3
"""
ACMG Classifier v0.5.0 - Com Logging + Exception Handling
=========================================================

ACMG/AMP 2015 + Validação Pydantic + Logging + Exceptions
"""
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import ValidationError

# Adicionar raiz do projeto ao Python PATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.variants.models import VariantInput
from src.utils import get_logger, VariantValidationError, ACMGClassificationError, FileProcessingError

# Configurar logger
logger = get_logger(__name__)


class ACMGCriteria:
    """Critérios ACMG/AMP 2015 para genes MMR"""
    
    PVS1_GENES = {
        "MLH1": ["deletion", "insertion", "stop_gained", "splice_site", "frameshift"],
        "MSH2": ["deletion", "insertion", "stop_gained", "splice_site", "frameshift"],
        "MSH6": ["deletion", "insertion", "stop_gained", "splice_site", "frameshift"],
        "PMS2": ["deletion", "insertion", "stop_gained", "splice_site", "frameshift"],
        "EPCAM": ["deletion", "insertion", "stop_gained", "splice_site", "frameshift"]
    }
    
    @staticmethod
    def check_pvs1(tipo: str, gene: str) -> bool:
        """PVS1: Null variant em gene MMR"""
        if gene not in ACMGCriteria.PVS1_GENES:
            return False
        return tipo in ACMGCriteria.PVS1_GENES[gene]
    
    @staticmethod
    def check_ps1(classificacao_original: str) -> bool:
        """PS1: Já reportado como Pathogenic"""
        return "Pathogenic" in classificacao_original and "Likely" not in classificacao_original
    
    @staticmethod
    def check_pm2(allele_frequency) -> bool:
        """PM2: Frequência muito baixa"""
        if not allele_frequency:
            return False
        try:
            freq = float(allele_frequency)
            return freq < 0.00001
        except ValueError:
            logger.warning(f"Frequência alélica inválida: {allele_frequency}")
            return False
    
    @staticmethod
    def check_ba1(allele_frequency) -> bool:
        """BA1: Frequência muito alta (benign)"""
        if not allele_frequency:
            return False
        try:
            freq = float(allele_frequency)
            return freq > 0.05
        except ValueError:
            logger.warning(f"Frequência alélica inválida: {allele_frequency}")
            return False


class ACMGClassifier:
    """Classificador ACMG/AMP 2015 para variantes MMR"""
    
    def __init__(self):
        self.logger = logger
    
    def classify(self, variant: VariantInput) -> str:
        """
        Classifica uma variante usando regras ACMG/AMP 2015.
        
        Retorna: "Pathogenic", "Likely Pathogenic", "VUS", "Likely Benign", "Benign"
        """
        try:
            self.logger.debug(f"Classificando variante: {variant.clinvar_id} ({variant.gene})")
            
            # Verificar critérios
            pvs1 = ACMGCriteria.check_pvs1(variant.tipo, variant.gene)
            ps1 = ACMGCriteria.check_ps1(variant.classificacao)
            pm2 = ACMGCriteria.check_pm2(variant.allele_frequency)
            ba1 = ACMGCriteria.check_ba1(variant.allele_frequency)
            
            # Aplicar regras ACMG
            if ba1:
                self.logger.info(f"{variant.clinvar_id}: BA1 ativado → BENIGN")
                return "Benign"
            
            if pvs1 and ps1:
                self.logger.info(f"{variant.clinvar_id}: PVS1 + PS1 → PATHOGENIC")
                return "Pathogenic"
            
            if pvs1 or (ps1 and pm2):
                self.logger.info(f"{variant.clinvar_id}: PVS1 ou PS1+PM2 → LIKELY PATHOGENIC")
                return "Likely Pathogenic"
            
            if pm2:
                self.logger.info(f"{variant.clinvar_id}: PM2 → VUS")
                return "VUS"
            
            self.logger.info(f"{variant.clinvar_id}: Sem critérios → VUS (default)")
            return "VUS"
        
        except Exception as e:
            self.logger.error(f"Erro ao classificar {variant.clinvar_id}: {str(e)}")
            raise ACMGClassificationError(f"Erro na classificação: {str(e)}")

    def classify_with_details(self, variant: dict) -> tuple:
        """ACMG/AMP 2015 com rastreabilidade: (class, criteria, confidence)."""
        criteria = []
        points = 0
        
        mutation_type = (variant.get("type") or variant.get("tipo") or "substitution").lower()
        if mutation_type in ["deletion", "insertion", "frameshift"]:
            criteria.append("PVS1")
            points += 4
        
        allele_freq = variant.get("allele_frequency") or 0.0001
        if allele_freq < 0.001:
            criteria.append("PM2")
            points += 1
        
        if allele_freq < 0.001 and mutation_type != "substitution":
            criteria.append("PP3")
            points += 1
        
        if points >= 6:
            pathogenicity_class = "PATHOGENIC"
            confidence = 0.95
        elif points >= 3:
            pathogenicity_class = "LIKELY_PATHOGENIC"
            confidence = 0.80
        else:
            pathogenicity_class = "VUS"
            confidence = 0.50
        
        return pathogenicity_class, criteria, confidence


def process_csv(input_file: str, output_file: str) -> int:
    """
    Processa arquivo CSV e gera classificações ACMG.
    
    Retorna: Número de variantes processadas
    """
    try:
        logger.info(f"Iniciando processamento de {input_file}")
        classifier = ACMGClassifier()
        
        variants_processadas = 0
        variants_erro = 0
        
        with open(input_file, "r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            
            with open(output_file, "w", encoding="utf-8", newline="") as outfile:
                fieldnames = ["clinvar_id", "gene", "hgvs", "tipo", "classificacao_acmg", "allele_frequency"]
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in reader:
                    try:
                        # Validar com Pydantic
                        variant = VariantInput(
                            clinvar_id=row.get("clinvar_id", ""),
                            gene=row.get("gene", ""),
                            hgvs=row.get("hgvs", ""),
                            classificacao=row.get("classificacao", ""),
                            tipo=row.get("tipo", ""),
                            allele_frequency=row.get("allele_frequency")
                        )
                        
                        # Classificar
                        classificacao_acmg = classifier.classify(variant)
                        
                        # Escrever resultado
                        writer.writerow({
                            "clinvar_id": variant.clinvar_id,
                            "gene": variant.gene,
                            "hgvs": variant.hgvs,
                            "tipo": variant.tipo,
                            "classificacao_acmg": classificacao_acmg,
                            "allele_frequency": variant.allele_frequency or "N/A"
                        })
                        
                        variants_processadas += 1
                    
                    except ValidationError as e:
                        logger.warning(f"Validação falhou para linha: {row}")
                        logger.warning(f"Erros: {e.errors()}")
                        variants_erro += 1
                    
                    except ACMGClassificationError as e:
                        logger.error(f"Erro na classificação: {e}")
                        variants_erro += 1
        
        logger.info(f"✅ Processamento concluído!")
        logger.info(f"   Variantes processadas: {variants_processadas}")
        logger.info(f"   Variantes com erro: {variants_erro}")
        logger.info(f"   Arquivo de saída: {output_file}")
        
        return variants_processadas
    
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {input_file}")
        raise FileProcessingError(f"Arquivo não encontrado: {input_file}")
    
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {str(e)}")
        raise FileProcessingError(f"Erro no processamento: {str(e)}")




def main() -> None:
    """Função main para execução do classificador ACMG"""
    print("\n" + "="*80)
    print("🧬 ACMG Classifier v0.5.0 - Com Logging + Exception Handling")
    print("="*80 + "\n")

    try:
        input_csv = "data/raw/clinvar_mmr_variants.csv"
        output_csv = "data/processed/clinvar_mmr_with_acmg_v0.5.0.csv"
    
        total = process_csv(input_csv, output_csv)
    
        print(f"✅ Sucesso! {total} variantes processadas.")
        print(f"📂 Resultado salvo em: {output_csv}")
        print(f"📝 Logs salvos em: logs/crispr_mmr_*.log")

    except FileProcessingError as e:
        print(f"❌ Erro no processamento: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

        print("\n" + "="*80 + "\n")

    if __name__ == "__main__":
        main()
