"""
Spiegazione direttiva 'from . import utils':
importa tutti i moduli importati in './utils/__init__.py'
"""

# Importo le variabili d'ambiente (ES: variabile 'env.APP_DEBUG' accessibile qui)
from . import env
# Importo gli utils
from . import utils
