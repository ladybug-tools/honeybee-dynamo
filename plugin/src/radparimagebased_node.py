# assign inputs
_complexity_, _recipeType_, radOptPar_, vmtxOptPar_, dmtxOptPar_, smtxOptPar_ = IN
radPar = vmtxPar = dmtxPar = smtxPar = None

try:
    from honeybee.radiance.recipe import parameters as param
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))
    

_complexity_ = _complexity_ or 0
_recipeType_ = _recipeType_ or 0

radPar, vmtxPar, dmtxPar, smtxPar = \
    param.get_radiance_parameters_image_based(_complexity_, _recipeType_)
    
if radOptPar_ and radPar:
    radPar.import_parameter_values_from_string(radOptPar_)

if vmtxOptPar_ and vmtxPar:
    vmtxPar.import_parameter_values_from_string(vmtxOptPar_)

if dmtxOptPar_ and dmtxPar:
    dmtxPar.import_parameter_values_from_string(dmtxOptPar_)

if smtxOptPar_ and smtxPar:
    smtxPar.import_parameter_values_from_string(smtxOptPar_)    

# assign outputs to OUT
OUT = radPar, vmtxPar, dmtxPar, smtxPar