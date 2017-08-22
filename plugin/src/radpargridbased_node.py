# assign inputs
_complexity_, _recipeType_, radOptPar_, vmtxOptPar_, dmtxOptPar_, smtxOptPar_ = IN
radPar = vmtxPar = dmtxPar = smtxPar = None

try:
    import honeybee.radiance.recipe.parameters as param
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))
    

_complexity_ = _complexity_ or 0
_recipeType_ = _recipeType_ or 0

radPar, vmtxPar, dmtxPar, smtxPar = \
    param.getRadianceParametersGridBased(_complexity_, _recipeType_)
    
if radOptPar_ and radPar:
    radPar.importParameterValuesFromString(radOptPar_)

if vmtxOptPar_ and vmtxPar:
    vmtxPar.importParameterValuesFromString(vmtxOptPar_)

if dmtxOptPar_ and dmtxPar:
    dmtxPar.importParameterValuesFromString(dmtxOptPar_)

if smtxOptPar_ and smtxPar:
    smtxPar.importParameterValuesFromString(smtxOptPar_)

# assign outputs to OUT
OUT = radPar, vmtxPar, dmtxPar, smtxPar