# This files keeps all enums as limits to how many object can be created per user. Premium tier will have higher limits!

class LIMITS:
  # DEPENDANT LIMITS
  ASSAY_LIMIT = 10
  CONTROL_LIMIT = 30
  ASSAY_CODE_LIMIT = 15
  BATCH_LIMIT = 30
  PROCESS_LIMIT = 15

  # INDEPENDANT LIMITS
  MAX_ASSAY_LIMIT = 1000
  MAX_CONTROL_LIMIT = 5000
  MAX_ASSAY_CODE_LIMIT = 2000
  MAX_BATCH_LIMIT = 50000
  MAX_PROCESS_LIMIT = 50000

  MAX_FLUORESCENCE_LIMIT = 100
  MAX_SAMPLES_PER_BATCH_LIMIT = 100
  MAX_EXTRACTION_PROTOCOL_LIMIT = 100
  MAX_THERMAL_CYCLER_PROTOCOL_LIMIT = 100
  MAX_LOCATION_LIMIT = 1000
  MAX_LADDER_LIMIT = 1000
  MAX_DYE_LIMIT = 1000
  MAX_PLATE_LIMIT = 1000
  MAX_GEL_LIMIT = 1000
  MAX_TUBE_LIMIT = 1000
  MAX_REAGENT_LIMIT = 1000