"""BOZZE auto-generate ALLA CIECA da generate_config_stubs.py - RIEMPI I TODO.
Lo script ha solo OSSERVATO i file: categoria, metodo, essential e keep sono
scelte tue. Il rename automatico copre solo i match ESATTI col CATALOG.
"""
from config import DatasetConfig


# ========================================================================
# ADAS
#   source: ADAS_28Oct2025.csv   |   righe campionate: 500   |   colonne: 16
#   INDIZIO categoria dal nome (NON deciso): ['scale']
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   115 | cand. ID
#     RID                      | num     |   115 | cand. ID
#     VISCODE                  | cat/str |     7 | cand. VISITA
#     VISCODE2                 | cat/str |     7 | cand. VISITA
#     VISDATE                  | date    |   305 | cand. DATA
#     TOTSCORE                 | num     |   112 | DA DECIDERE
#     TOTAL13                  | num     |   140 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |     1 | cand. DATA
#     USERDATE2                | vuota   |     0 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
ADAS = DatasetConfig(
    file_code="ADAS",                          # <-- VERIFICA
    source="ADAS_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['scale'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['VISDATE', 'update_stamp']) VERIFICA
    # 3 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['TOTSCORE', 'TOTAL13', 'USERDATE2']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ADNI_DIAN_COMPARISON_STUDY_DATA_SUBSET_05_23_22
#   source: ADNI-DIAN_Comparison_Study_Data_Subset_05_23_22_23Oct2025.csv   |   righe campionate: 500   |   colonne: 134
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     COLPROT                  | cat/str |     4 | DA DECIDERE
#     RID                      | num     |    53 | cand. ID
#     VISCODE                  | cat/str |     7 | cand. VISITA
#     VISCODE2                 | cat/str |    14 | cand. VISITA
#     EXAMDATE                 | date    |   433 | cand. DATA
#     VISITAGE                 | num     |   493 | DA DECIDERE
#     CDRGLOB                  | num     |     5 | DA DECIDERE
#     CSFDATE                  | date    |    38 | cand. DATA
#     EDUC                     | num     |    10 | DA DECIDERE
#     MRI_SCANDATE             | date    |    77 | cand. DATA
#     FLUF                     | num     |    25 | DA DECIDERE
#     WORDIM                   | num     |    16 | DA DECIDERE
#     LOGIMEM                  | num     |    23 | DA DECIDERE
#     DIGIF                    | num     |    10 | DA DECIDERE
#     DIGIFLEN                 | num     |     6 | DA DECIDERE
#     DIGIB                    | num     |    11 | DA DECIDERE
#     DIGIBLEN                 | num     |     6 | DA DECIDERE
#     ANIMALS                  | num     |    32 | DA DECIDERE
#     VEG                      | num     |    26 | DA DECIDERE
#     TRAILA                   | num     |    89 | DA DECIDERE
#     TRAILARR                 | num     |     4 | DA DECIDERE
#     TRAILB                   | num     |   149 | DA DECIDERE
#     TRAILBRR                 | num     |     9 | DA DECIDERE
#     WAIS                     | num     |    58 | DA DECIDERE
#     MEMUNITS                 | num     |    23 | DA DECIDERE
#     BOSTON                   | num     |    25 | DA DECIDERE
#     WORDDEL                  | num     |    16 | DA DECIDERE
#     MR_TOTV_WMHYPOINTENSITIES | num     |    79 | DA DECIDERE
#     MR_TOTV_INTRACRANIAL     | num     |    79 | DA DECIDERE
#     MR_TOTV_HIPPOCAMPUS      | num     |    79 | DA DECIDERE
#     FDG_FSUVR_RSF_TOT_CTX_PRECUNEUS | num     |    13 | DA DECIDERE
#     FDG_FSUVR_RSF_TOT_HIPPOCAMPUS | num     |    13 | DA DECIDERE
#     FDG_FSUVR_RSF_TOT_CORTMEAN | num     |    12 | DA DECIDERE
#     PIB_FSUVR_RSF_TOT_CTX_PRECUNEUS | num     |     7 | DA DECIDERE
#     PIB_FSUVR_RSF_TOT_HIPPOCAMPUS | num     |     7 | DA DECIDERE
#     PIB_FSUVR_RSF_TOT_CORTMEAN | num     |     8 | DA DECIDERE
#     BIRTHMO                  | num     |    12 | DA DECIDERE
#     BIRTHYR                  | num     |    25 | DA DECIDERE
#     HISPANIC                 | num     |     1 | DA DECIDERE
#     RACE                     | num     |     3 | DA DECIDERE
#     PRIMLANG                 | num     |     1 | DA DECIDERE
#     MARISTAT                 | num     |     3 | DA DECIDERE
#     HANDED                   | num     |     2 | DA DECIDERE
#     MOMDEM                   | num     |     2 | DA DECIDERE
#     MOMAUTO                  | num     |     2 | DA DECIDERE
#     DADDEM                   | num     |     2 | DA DECIDERE
#     DADAUTO                  | num     |     2 | DA DECIDERE
#     ABRUPT                   | num     |     1 | DA DECIDERE
#     STEPWISE                 | num     |     2 | DA DECIDERE
#     SOMATIC                  | num     |     2 | DA DECIDERE
#     EMOT                     | num     |     2 | DA DECIDERE
#     HXHYPER                  | num     |     2 | DA DECIDERE
#     HXSTROKE                 | num     |     2 | DA DECIDERE
#     FOCLSYM                  | num     |     2 | DA DECIDERE
#     FOCLSIGN                 | num     |     2 | DA DECIDERE
#     HACHIN                   | num     |     4 | DA DECIDERE
#     CDRSUM                   | num     |    24 | DA DECIDERE
#     GDS                      | num     |    12 | DA DECIDERE
#     BILLS                    | num     |     6 | DA DECIDERE
#     TAXES                    | num     |     6 | DA DECIDERE
#     SHOPPING                 | num     |     6 | DA DECIDERE
#     GAMES                    | num     |     6 | DA DECIDERE
#     STOVE                    | num     |     6 | DA DECIDERE
#     MEALPREP                 | num     |     6 | DA DECIDERE
#     EVENTS                   | num     |     6 | DA DECIDERE
#     PAYATTN                  | num     |     5 | DA DECIDERE
#     REMDATES                 | num     |     6 | DA DECIDERE
#     TRAVEL                   | num     |     6 | DA DECIDERE
#     DECSUB                   | num     |     2 | DA DECIDERE
#     VASC                     | num     |     2 | DA DECIDERE
#     ALCDEM                   | num     |     1 | DA DECIDERE
#     FTD                      | num     |     1 | DA DECIDERE
#     PPAPH                    | num     |     1 | DA DECIDERE
#     PSP                      | num     |     1 | DA DECIDERE
#     CORT                     | num     |     2 | DA DECIDERE
#     HUNT                     | num     |     1 | DA DECIDERE
#     PRION                    | num     |     1 | DA DECIDERE
#     DEP                      | num     |     1 | DA DECIDERE
#     PARK                     | num     |     1 | DA DECIDERE
#     HYCEPH                   | num     |     2 | DA DECIDERE
#     COGOTH                   | num     |     2 | DA DECIDERE
#     COGOTHX                  | cat/str |     1 | DA DECIDERE
#     GENDER                   | num     |     2 | DA DECIDERE
#     CSF_ELC_AB42             | num     |    38 | DA DECIDERE
#     CSF_ELC_PTAU             | num     |    36 | DA DECIDERE
#     CSF_ELC_TAU              | num     |    36 | DA DECIDERE
#     CSF_ELC_AB40             | num     |    39 | DA DECIDERE
#     CSF_ELC_AB4240           | num     |    35 | DA DECIDERE
#     MSP_AB38                 | num     |    39 | DA DECIDERE
#     MSP_AB40                 | num     |    39 | DA DECIDERE
#     MSP_AB42                 | num     |    38 | DA DECIDERE
#     CSF_DATE_BL              | date    |    13 | cand. DATA
#     MRI_DATE_BL              | date    |    30 | cand. DATA
#     CSF_CDR_BL               | num     |     3 | DA DECIDERE
#     MRI_CDR_BL               | num     |     3 | DA DECIDERE
#     CSF_CDRSB_BL             | num     |    10 | DA DECIDERE
#     MRI_CDRSB_BL             | num     |    12 | DA DECIDERE
#     VISIT_DATE_BL            | date    |    43 | cand. DATA
#     MR_TOTT_PRECUNEUS        | num     |    78 | DA DECIDERE
#     LAST_VISIT_DATE          | date    |    50 | cand. DATA
#     TIME_COGNITIVE_FOLLOWUP  | num     |    53 | DA DECIDERE
#     TIME_CSF_FOLLOWUP        | num     |    13 | DA DECIDERE
#     TIME_MRI_FOLLOWUP        | num     |    31 | DA DECIDERE
#     CDR_BASELINE             | num     |     3 | DA DECIDERE
#     GROUP_CSF                | num     |     5 | DA DECIDERE
#     GROUP_MRI                | num     |     6 | DA DECIDERE
#     COHORT                   | num     |     1 | DA DECIDERE
#     PET_TYPE                 | cat/str |     3 | DA DECIDERE
#     PIB_MSUVR_TOT_PRECUNEUS  | vuota   |     0 | DA DECIDERE
#     PIB_MSUVR_TOT_CORTMEAN   | vuota   |     0 | DA DECIDERE
#     FDG_MSUVR_TOT_PRECUNEUS  | num     |     1 | DA DECIDERE
#     FDG_MSUVR_TOT_CORTMEAN   | num     |     1 | DA DECIDERE
#     AV45_FSUVR_RSF_TOT_CTX_PRECUNEUS | num     |    32 | DA DECIDERE
#     AV45_FSUVR_RSF_TOT_HIPPOCAMPUS | num     |    31 | DA DECIDERE
#     AV45_FSUVR_RSF_TOT_CORTMEAN | num     |    32 | DA DECIDERE
#     AV45_MSUVR_TOT_PRECUNEUS | num     |     9 | DA DECIDERE
#     AV45_MSUVR_TOT_CORTMEAN  | num     |    10 | DA DECIDERE
#     PET_DATE_BL              | date    |    14 | cand. DATA
#     PET_CDR_BL               | num     |     3 | DA DECIDERE
#     PET_CDRSB_BL             | num     |    10 | DA DECIDERE
#     TIME_PET_FOLLOWUP        | num     |    14 | DA DECIDERE
#     ADGROUP                  | num     |     2 | DA DECIDERE
#     ADGROUP_BL               | num     |     2 | DA DECIDERE
#     GROUP_PET                | num     |     5 | DA DECIDERE
#     PET_SCANDATE             | date    |    40 | cand. DATA
#     ORIGIN                   | cat/str |     1 | DA DECIDERE
#     DIAN_ID                  | num     |    53 | cand. ID
#     DIAN_APOE                | num     |     5 | DA DECIDERE
#     DIAN_GROUP               | num     |     4 | DA DECIDERE
#     DIAN_CDRSB_BL            | num     |     8 | DA DECIDERE
#     DIAN_YEARS_BL            | num     |   325 | DA DECIDERE
#     DIAN_MMSE                | num     |    23 | DA DECIDERE
#     NEYO                     | num     |   440 | DA DECIDERE
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
ADNI_DIAN_COMPARISON_STUDY_DATA_SUBSET_05_23_22 = DatasetConfig(
    file_code="ADNI-DIAN_Comparison_Study_Data_Subset_05_23_22",                          # <-- VERIFICA
    source="ADNI-DIAN_Comparison_Study_Data_Subset_05_23_22_23Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['DIAN_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['CSFDATE', 'MRI_SCANDATE', 'CSF_DATE_BL', 'MRI_DATE_BL', 'VISIT_DATE_BL', 'LAST_VISIT_DATE', 'PET_DATE_BL', 'PET_SCANDATE', 'update_stamp']) VERIFICA
    # 120 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['COLPROT', 'VISITAGE', 'CDRGLOB', 'EDUC', 'FLUF', 'WORDIM', 'LOGIMEM', 'DIGIF', 'DIGIFLEN', 'DIGIB', 'DIGIBLEN', 'ANIMALS', 'VEG', 'TRAILA', 'TRAILARR', 'TRAILB', 'TRAILBRR', 'WAIS', 'MEMUNITS', 'BOSTON', 'WORDDEL', 'MR_TOTV_WMHYPOINTENSITIES', 'MR_TOTV_INTRACRANIAL', 'MR_TOTV_HIPPOCAMPUS', 'FDG_FSUVR_RSF_TOT_CTX_PRECUNEUS', 'FDG_FSUVR_RSF_TOT_HIPPOCAMPUS', 'FDG_FSUVR_RSF_TOT_CORTMEAN', 'PIB_FSUVR_RSF_TOT_CTX_PRECUNEUS', 'PIB_FSUVR_RSF_TOT_HIPPOCAMPUS', 'PIB_FSUVR_RSF_TOT_CORTMEAN', 'BIRTHMO', 'BIRTHYR', 'HISPANIC', 'RACE', 'PRIMLANG', 'MARISTAT', 'HANDED', 'MOMDEM', 'MOMAUTO', 'DADDEM', 'DADAUTO', 'ABRUPT', 'STEPWISE', 'SOMATIC', 'EMOT', 'HXHYPER', 'HXSTROKE', 'FOCLSYM', 'FOCLSIGN', 'HACHIN', 'CDRSUM', 'GDS', 'BILLS', 'TAXES', 'SHOPPING', 'GAMES', 'STOVE', 'MEALPREP', 'EVENTS', 'PAYATTN', 'REMDATES', 'TRAVEL', 'DECSUB', 'VASC', 'ALCDEM', 'FTD', 'PPAPH', 'PSP', 'CORT', 'HUNT', 'PRION', 'DEP', 'PARK', 'HYCEPH', 'COGOTH', 'COGOTHX', 'GENDER', 'CSF_ELC_AB42', 'CSF_ELC_PTAU', 'CSF_ELC_TAU', 'CSF_ELC_AB40', 'CSF_ELC_AB4240', 'MSP_AB38', 'MSP_AB40', 'MSP_AB42', 'CSF_CDR_BL', 'MRI_CDR_BL', 'CSF_CDRSB_BL', 'MRI_CDRSB_BL', 'MR_TOTT_PRECUNEUS', 'TIME_COGNITIVE_FOLLOWUP', 'TIME_CSF_FOLLOWUP', 'TIME_MRI_FOLLOWUP', 'CDR_BASELINE', 'GROUP_CSF', 'GROUP_MRI', 'COHORT', 'PET_TYPE', 'PIB_MSUVR_TOT_PRECUNEUS', 'PIB_MSUVR_TOT_CORTMEAN', 'FDG_MSUVR_TOT_PRECUNEUS', 'FDG_MSUVR_TOT_CORTMEAN', 'AV45_FSUVR_RSF_TOT_CTX_PRECUNEUS', 'AV45_FSUVR_RSF_TOT_HIPPOCAMPUS', 'AV45_FSUVR_RSF_TOT_CORTMEAN', 'AV45_MSUVR_TOT_PRECUNEUS', 'AV45_MSUVR_TOT_CORTMEAN', 'PET_CDR_BL', 'PET_CDRSB_BL', 'TIME_PET_FOLLOWUP', 'ADGROUP', 'ADGROUP_BL', 'GROUP_PET', 'ORIGIN', 'DIAN_APOE', 'DIAN_GROUP', 'DIAN_CDRSB_BL', 'DIAN_YEARS_BL', 'DIAN_MMSE', 'NEYO']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ADNIMERGE
#   source: ADNIMERGE_05Mar2026.csv   |   righe campionate: 500   |   colonne: 116
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   123 | cand. ID
#     COLPROT                  | cat/str |     3 | DA DECIDERE
#     ORIGPROT                 | cat/str |     2 | DA DECIDERE
#     PTID                     | cat/str |   123 | cand. ID
#     SITE                     | num     |    30 | DA DECIDERE
#     VISCODE                  | cat/str |     9 | cand. VISITA
#     EXAMDATE                 | date    |   370 | cand. DATA
#     DX_bl                    | cat/str |     4 | DA DECIDERE
#     AGE                      | num     |    97 | DA DECIDERE
#     PTGENDER                 | cat/str |     2 | DA DECIDERE
#     PTEDUCAT                 | num     |    12 | DA DECIDERE
#     PTETHCAT                 | cat/str |     2 | DA DECIDERE
#     PTRACCAT                 | cat/str |     4 | DA DECIDERE
#     PTMARRY                  | cat/str |     4 | DA DECIDERE
#     APOE4                    | num     |     3 | DA DECIDERE
#     FDG                      | num     |   194 | DA DECIDERE
#     PIB                      | num     |    14 | DA DECIDERE
#     AV45                     | num     |    23 | DA DECIDERE
#     FBB                      | vuota   |     0 | DA DECIDERE
#     ABETA                    | num     |   127 | DA DECIDERE
#     TAU                      | num     |   128 | DA DECIDERE
#     PTAU                     | num     |   126 | DA DECIDERE
#     CDRSB                    | num     |    21 | DA DECIDERE
#     ADAS11                   | num     |    95 | DA DECIDERE
#     ADAS13                   | num     |   130 | DA DECIDERE
#     ADASQ4                   | num     |    11 | DA DECIDERE
#     MMSE                     | num     |    20 | DA DECIDERE
#     RAVLT_immediate          | num     |    63 | DA DECIDERE
#     RAVLT_learning           | num     |    16 | DA DECIDERE
#     RAVLT_forgetting         | num     |    17 | DA DECIDERE
#     RAVLT_perc_forgetting    | num     |    68 | DA DECIDERE
#     LDELTOTAL                | num     |    25 | DA DECIDERE
#     DIGITSCOR                | num     |    65 | DA DECIDERE
#     TRABSCOR                 | num     |   143 | DA DECIDERE
#     FAQ                      | num     |    31 | DA DECIDERE
#     MOCA                     | num     |    12 | DA DECIDERE
#     EcogPtMem                | num     |    13 | DA DECIDERE
#     EcogPtLang               | num     |    13 | DA DECIDERE
#     EcogPtVisspat            | num     |     5 | DA DECIDERE
#     EcogPtPlan               | num     |     5 | DA DECIDERE
#     EcogPtOrgan              | num     |     9 | DA DECIDERE
#     EcogPtDivatt             | num     |     6 | DA DECIDERE
#     EcogPtTotal              | num     |    24 | DA DECIDERE
#     EcogSPMem                | num     |    13 | DA DECIDERE
#     EcogSPLang               | num     |     8 | DA DECIDERE
#     EcogSPVisspat            | num     |     8 | DA DECIDERE
#     EcogSPPlan               | num     |     7 | DA DECIDERE
#     EcogSPOrgan              | num     |     9 | DA DECIDERE
#     EcogSPDivatt             | num     |     8 | DA DECIDERE
#     EcogSPTotal              | num     |    23 | DA DECIDERE
#     FLDSTRENG                | cat/str |     2 | DA DECIDERE
#     Ventricles               | num     |   484 | DA DECIDERE
#     Hippocampus              | num     |   460 | DA DECIDERE
#     WholeBrain               | num     |   485 | DA DECIDERE
#     Entorhinal               | num     |   450 | DA DECIDERE
#     Fusiform                 | num     |   474 | DA DECIDERE
#     MidTemp                  | num     |   475 | DA DECIDERE
#     ICV                      | num     |   485 | DA DECIDERE
#     DX                       | cat/str |     3 | DA DECIDERE
#     mPACCdigit               | num     |   487 | DA DECIDERE
#     mPACCtrailsB             | num     |   482 | DA DECIDERE
#     EXAMDATE_bl              | date    |    84 | cand. DATA
#     CDRSB_bl                 | num     |    13 | DA DECIDERE
#     ADAS11_bl                | num     |    57 | DA DECIDERE
#     ADAS13_bl                | num     |    69 | DA DECIDERE
#     ADASQ4_bl                | num     |    11 | DA DECIDERE
#     MMSE_bl                  | num     |    11 | DA DECIDERE
#     RAVLT_immediate_bl       | num     |    44 | DA DECIDERE
#     RAVLT_learning_bl        | num     |    13 | DA DECIDERE
#     RAVLT_forgetting_bl      | num     |    14 | DA DECIDERE
#     RAVLT_perc_forgetting_bl | num     |    44 | DA DECIDERE
#     LDELTOTAL_BL             | num     |    22 | DA DECIDERE
#     DIGITSCOR_bl             | num     |    47 | DA DECIDERE
#     TRABSCOR_bl              | num     |    78 | DA DECIDERE
#     FAQ_bl                   | num     |    18 | DA DECIDERE
#     mPACCdigit_bl            | num     |   123 | DA DECIDERE
#     mPACCtrailsB_bl          | num     |   121 | DA DECIDERE
#     FLDSTRENG_bl             | cat/str |     2 | DA DECIDERE
#     FSVERSION_bl             | cat/str |     2 | DA DECIDERE
#     IMAGEUID_bl              | num     |   123 | DA DECIDERE
#     Ventricles_bl            | num     |   121 | DA DECIDERE
#     Hippocampus_bl           | num     |   106 | DA DECIDERE
#     WholeBrain_bl            | num     |   121 | DA DECIDERE
#     Entorhinal_bl            | num     |   101 | DA DECIDERE
#     Fusiform_bl              | num     |   101 | DA DECIDERE
#     MidTemp_bl               | num     |   104 | DA DECIDERE
#     ICV_bl                   | num     |   123 | DA DECIDERE
#     MOCA_bl                  | num     |     6 | DA DECIDERE
#     EcogPtMem_bl             | num     |     5 | DA DECIDERE
#     EcogPtLang_bl            | num     |     5 | DA DECIDERE
#     EcogPtVisspat_bl         | num     |     3 | DA DECIDERE
#     EcogPtPlan_bl            | num     |     3 | DA DECIDERE
#     EcogPtOrgan_bl           | num     |     6 | DA DECIDERE
#     EcogPtDivatt_bl          | num     |     5 | DA DECIDERE
#     EcogPtTotal_bl           | num     |     8 | DA DECIDERE
#     EcogSPMem_bl             | num     |     6 | DA DECIDERE
#     EcogSPLang_bl            | num     |     5 | DA DECIDERE
#     EcogSPVisspat_bl         | num     |     4 | DA DECIDERE
#     EcogSPPlan_bl            | num     |     3 | DA DECIDERE
#     EcogSPOrgan_bl           | num     |     5 | DA DECIDERE
#     EcogSPDivatt_bl          | num     |     5 | DA DECIDERE
#     EcogSPTotal_bl           | num     |     8 | DA DECIDERE
#     ABETA_bl                 | num     |    69 | DA DECIDERE
#     TAU_bl                   | num     |    68 | DA DECIDERE
#     PTAU_bl                  | num     |    69 | DA DECIDERE
#     FDG_bl                   | num     |    53 | DA DECIDERE
#     PIB_bl                   | vuota   |     0 | DA DECIDERE
#     AV45_bl                  | num     |     9 | DA DECIDERE
#     FBB_bl                   | vuota   |     0 | DA DECIDERE
#     Years_bl                 | num     |   196 | DA DECIDERE
#     Month_bl                 | num     |   196 | DA DECIDERE
#     Month                    | num     |    12 | DA DECIDERE
#     M                        | num     |     9 | DA DECIDERE
#     update_stamp             | date    |     5 | cand. DATA
# ------------------------------------------------------------------------
ADNIMERGE = DatasetConfig(
    file_code="ADNIMERGE",                          # <-- VERIFICA
    source="ADNIMERGE_05Mar2026.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['EXAMDATE_bl', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 108 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['COLPROT', 'ORIGPROT', 'SITE', 'DX_bl', 'AGE', 'PTGENDER', 'PTEDUCAT', 'PTETHCAT', 'PTRACCAT', 'PTMARRY', 'APOE4', 'FDG', 'PIB', 'AV45', 'FBB', 'ABETA', 'TAU', 'PTAU', 'CDRSB', 'ADAS11', 'ADAS13', 'ADASQ4', 'MMSE', 'RAVLT_immediate', 'RAVLT_learning', 'RAVLT_forgetting', 'RAVLT_perc_forgetting', 'LDELTOTAL', 'DIGITSCOR', 'TRABSCOR', 'FAQ', 'MOCA', 'EcogPtMem', 'EcogPtLang', 'EcogPtVisspat', 'EcogPtPlan', 'EcogPtOrgan', 'EcogPtDivatt', 'EcogPtTotal', 'EcogSPMem', 'EcogSPLang', 'EcogSPVisspat', 'EcogSPPlan', 'EcogSPOrgan', 'EcogSPDivatt', 'EcogSPTotal', 'FLDSTRENG', 'Ventricles', 'Hippocampus', 'WholeBrain', 'Entorhinal', 'Fusiform', 'MidTemp', 'ICV', 'DX', 'mPACCdigit', 'mPACCtrailsB', 'CDRSB_bl', 'ADAS11_bl', 'ADAS13_bl', 'ADASQ4_bl', 'MMSE_bl', 'RAVLT_immediate_bl', 'RAVLT_learning_bl', 'RAVLT_forgetting_bl', 'RAVLT_perc_forgetting_bl', 'LDELTOTAL_BL', 'DIGITSCOR_bl', 'TRABSCOR_bl', 'FAQ_bl', 'mPACCdigit_bl', 'mPACCtrailsB_bl', 'FLDSTRENG_bl', 'FSVERSION_bl', 'IMAGEUID_bl', 'Ventricles_bl', 'Hippocampus_bl', 'WholeBrain_bl', 'Entorhinal_bl', 'Fusiform_bl', 'MidTemp_bl', 'ICV_bl', 'MOCA_bl', 'EcogPtMem_bl', 'EcogPtLang_bl', 'EcogPtVisspat_bl', 'EcogPtPlan_bl', 'EcogPtOrgan_bl', 'EcogPtDivatt_bl', 'EcogPtTotal_bl', 'EcogSPMem_bl', 'EcogSPLang_bl', 'EcogSPVisspat_bl', 'EcogSPPlan_bl', 'EcogSPOrgan_bl', 'EcogSPDivatt_bl', 'EcogSPTotal_bl', 'ABETA_bl', 'TAU_bl', 'PTAU_bl', 'FDG_bl', 'PIB_bl', 'AV45_bl', 'FBB_bl', 'Years_bl', 'Month_bl', 'Month', 'M']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ADNI_BLENNOWPLASMANFLLONG_10_03_18
#   source: ADNI_BLENNOWPLASMANFLLONG_10_03_18_11Aug2025.csv   |   righe campionate: 500   |   colonne: 11
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   146 | cand. ID
#     VISCODE                  | cat/str |    13 | cand. VISITA
#     VISCODE2                 | cat/str |    12 | cand. VISITA
#     USERDATE                 | date    |     1 | cand. DATA
#     EXAMDATE                 | date    |   389 | cand. DATA
#     DRAW_DATE                | date    |   392 | cand. DATA
#     DRAW_TIME                | date    |   204 | cand. DATA
#     PLASMA_NFL               | num     |   377 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
ADNI_BLENNOWPLASMANFLLONG_10_03_18 = DatasetConfig(
    file_code="ADNI_BLENNOWPLASMANFLLONG_10_03_18",                          # <-- VERIFICA
    source="ADNI_BLENNOWPLASMANFLLONG_10_03_18_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['USERDATE', 'DRAW_DATE', 'DRAW_TIME', 'update_stamp']) VERIFICA
    # 1 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['PLASMA_NFL']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ADNI_EUROIMMUN
#   source: ADNI_EUROIMMUN_11Aug2025.csv   |   righe campionate: 280   |   colonne: 11
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     9 | cand. VISITA
#     VISCODE2                 | cat/str |     7 | cand. VISITA
#     EXAMDATE                 | date    |   107 | cand. DATA
#     POOL                     | cat/str |     2 | DA DECIDERE
#     DRAWTIME                 | date    |     9 | cand. DATA
#     COMMENTS                 | cat/str |     3 | DA DECIDERE
#     BETA_AMYLOID_1_40        | num     |   139 | DA DECIDERE
#     BETA_AMYLOID_1_42        | num     |   139 | DA DECIDERE
#     BETA_AMYLOID_42_40       | num     |   139 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
ADNI_EUROIMMUN = DatasetConfig(
    file_code="ADNI_EUROIMMUN",                          # <-- VERIFICA
    source="ADNI_EUROIMMUN_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWTIME', 'update_stamp']) VERIFICA
    # 5 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['POOL', 'COMMENTS', 'BETA_AMYLOID_1_40', 'BETA_AMYLOID_1_42', 'BETA_AMYLOID_42_40']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ADNI_LIPIDOMICSRADER
#   source: ADNI_LIPIDOMICSRADER_09Oct2025.csv   |   righe campionate: 500   |   colonne: 11
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     ORIGPROT                 | cat/str |     1 | DA DECIDERE
#     COLPROT                  | cat/str |     1 | DA DECIDERE
#     RID                      | num     |   500 | cand. ID
#     VISCODE                  | cat/str |     1 | cand. VISITA
#     VISCODE2                 | cat/str |     1 | cand. VISITA
#     CHOL                     | num     |   154 | DA DECIDERE
#     HDL                      | num     |    79 | DA DECIDERE
#     TG                       | num     |   190 | DA DECIDERE
#     APOA1                    | num     |   124 | DA DECIDERE
#     APOE                     | num     |    69 | censure >/<, DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
ADNI_LIPIDOMICSRADER = DatasetConfig(
    file_code="ADNI_LIPIDOMICSRADER",                          # <-- VERIFICA
    source="ADNI_LIPIDOMICSRADER_09Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="update_stamp",                  # rilevato dai valori, VERIFICA
    # 7 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['ORIGPROT', 'COLPROT', 'CHOL', 'HDL', 'TG', 'APOA1', 'APOE']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ADNI_PICSLASHS
#   source: ADNI_PICSLASHS_28Oct2025.csv   |   righe campionate: 500   |   colonne: 67
#   ignorate 4 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   193 | cand. ID
#     RID                      | num     |   193 | cand. ID
#     VISCODE                  | cat/str |    15 | cand. VISITA
#     VISCODE2                 | cat/str |    32 | cand. VISITA
#     EXAMDATE                 | date    |   444 | cand. DATA
#     PROCESSDATE              | date    |     1 | cand. DATA
#     IMAGEUID_T1              | num     |   500 | DA DECIDERE
#     IMAGEUID_T2              | num     |   500 | DA DECIDERE
#     LEFT_CA1_VOL             | num     |   483 | DA DECIDERE
#     LEFT_CA1_NS              | num     |    17 | DA DECIDERE
#     LEFT_CA2_VOL             | num     |    35 | DA DECIDERE
#     LEFT_CA2_NS              | num     |     9 | DA DECIDERE
#     LEFT_CA3_VOL             | num     |   303 | DA DECIDERE
#     LEFT_CA3_NS              | num     |    10 | DA DECIDERE
#     LEFT_DG_VOL              | num     |   474 | DA DECIDERE
#     LEFT_DG_NS               | num     |    16 | DA DECIDERE
#     LEFT_MISC_VOL            | num     |   447 | DA DECIDERE
#     LEFT_MISC_NS             | num     |    18 | DA DECIDERE
#     LEFT_SUB_VOL             | num     |   441 | DA DECIDERE
#     LEFT_SUB_NS              | num     |    16 | DA DECIDERE
#     LEFT_ERC_VOL             | num     |   457 | DA DECIDERE
#     LEFT_ERC_NS              | num     |    11 | DA DECIDERE
#     LEFT_BA35_VOL            | num     |   464 | DA DECIDERE
#     LEFT_BA35_NS             | num     |    11 | DA DECIDERE
#     LEFT_BA36_VOL            | num     |   484 | DA DECIDERE
#     LEFT_BA36_NS             | num     |    11 | DA DECIDERE
#     LEFT_PHC_VOL             | num     |   471 | DA DECIDERE
#     LEFT_PHC_NS              | num     |    10 | DA DECIDERE
#     LEFT_SULCUS_VOL          | num     |   461 | DA DECIDERE
#     LEFT_SULCUS_NS           | num     |    15 | DA DECIDERE
#     LEFT_CA_VOL              | num     |   485 | DA DECIDERE
#     LEFT_CA_NS               | num     |    17 | DA DECIDERE
#     LEFT_HIPP_VOL            | num     |   489 | DA DECIDERE
#     LEFT_HIPP_NS             | num     |    17 | DA DECIDERE
#     RIGHT_CA1_VOL            | num     |   480 | DA DECIDERE
#     RIGHT_CA1_NS             | num     |    18 | DA DECIDERE
#     RIGHT_CA2_VOL            | num     |   120 | DA DECIDERE
#     RIGHT_CA2_NS             | num     |    10 | DA DECIDERE
#     RIGHT_CA3_VOL            | num     |   310 | DA DECIDERE
#     RIGHT_CA3_NS             | num     |     8 | DA DECIDERE
#     RIGHT_DG_VOL             | num     |   473 | DA DECIDERE
#     RIGHT_DG_NS              | num     |    16 | DA DECIDERE
#     RIGHT_MISC_VOL           | num     |   398 | DA DECIDERE
#     RIGHT_MISC_NS            | num     |    20 | DA DECIDERE
#     RIGHT_SUB_VOL            | num     |   447 | DA DECIDERE
#     RIGHT_SUB_NS             | num     |    17 | DA DECIDERE
#     RIGHT_ERC_VOL            | num     |   459 | DA DECIDERE
#     RIGHT_ERC_NS             | num     |     9 | DA DECIDERE
#     RIGHT_BA35_VOL           | num     |   458 | DA DECIDERE
#     RIGHT_BA35_NS            | num     |     9 | DA DECIDERE
#     RIGHT_BA36_VOL           | num     |   483 | DA DECIDERE
#     RIGHT_BA36_NS            | num     |     7 | DA DECIDERE
#     RIGHT_PHC_VOL            | num     |   477 | DA DECIDERE
#     RIGHT_PHC_NS             | num     |    10 | DA DECIDERE
#     RIGHT_SULCUS_VOL         | num     |   462 | DA DECIDERE
#     RIGHT_SULCUS_NS          | num     |    17 | DA DECIDERE
#     RIGHT_CA_VOL             | num     |   485 | DA DECIDERE
#     RIGHT_CA_NS              | num     |    18 | DA DECIDERE
#     RIGHT_HIPP_VOL           | num     |   485 | DA DECIDERE
#     RIGHT_HIPP_NS            | num     |    18 | DA DECIDERE
#     ICV                      | num     |   500 | DA DECIDERE
#     SLICE_THICKNESS          | num     |    27 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
ADNI_PICSLASHS = DatasetConfig(
    file_code="ADNI_PICSLASHS",                          # <-- VERIFICA
    source="ADNI_PICSLASHS_28Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['PROCESSDATE', 'update_stamp']) VERIFICA
    # 56 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['IMAGEUID_T1', 'IMAGEUID_T2', 'LEFT_CA1_VOL', 'LEFT_CA1_NS', 'LEFT_CA2_VOL', 'LEFT_CA2_NS', 'LEFT_CA3_VOL', 'LEFT_CA3_NS', 'LEFT_DG_VOL', 'LEFT_DG_NS', 'LEFT_MISC_VOL', 'LEFT_MISC_NS', 'LEFT_SUB_VOL', 'LEFT_SUB_NS', 'LEFT_ERC_VOL', 'LEFT_ERC_NS', 'LEFT_BA35_VOL', 'LEFT_BA35_NS', 'LEFT_BA36_VOL', 'LEFT_BA36_NS', 'LEFT_PHC_VOL', 'LEFT_PHC_NS', 'LEFT_SULCUS_VOL', 'LEFT_SULCUS_NS', 'LEFT_CA_VOL', 'LEFT_CA_NS', 'LEFT_HIPP_VOL', 'LEFT_HIPP_NS', 'RIGHT_CA1_VOL', 'RIGHT_CA1_NS', 'RIGHT_CA2_VOL', 'RIGHT_CA2_NS', 'RIGHT_CA3_VOL', 'RIGHT_CA3_NS', 'RIGHT_DG_VOL', 'RIGHT_DG_NS', 'RIGHT_MISC_VOL', 'RIGHT_MISC_NS', 'RIGHT_SUB_VOL', 'RIGHT_SUB_NS', 'RIGHT_ERC_VOL', 'RIGHT_ERC_NS', 'RIGHT_BA35_VOL', 'RIGHT_BA35_NS', 'RIGHT_BA36_VOL', 'RIGHT_BA36_NS', 'RIGHT_PHC_VOL', 'RIGHT_PHC_NS', 'RIGHT_SULCUS_VOL', 'RIGHT_SULCUS_NS', 'RIGHT_CA_VOL', 'RIGHT_CA_NS', 'RIGHT_HIPP_VOL', 'RIGHT_HIPP_NS', 'ICV', 'SLICE_THICKNESS']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ADSP_PHC_BIOMARKER
#   source: ADSP_PHC_BIOMARKER_25Jul2025.csv   |   righe campionate: 500   |   colonne: 26
#   ignorate 1 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   500 | cand. ID
#     PTID                     | cat/str |   500 | cand. ID
#     SUBJID                   | cat/str |   465 | DA DECIDERE
#     VISCODE                  | cat/str |     9 | cand. VISITA
#     VISCODE2                 | cat/str |     8 | cand. VISITA
#     DRAWDATE                 | date    |   410 | cand. DATA
#     PHC_Visit                | num     |    10 | DA DECIDERE
#     PHC_Age_Biomarker        | num     |   457 | DA DECIDERE
#     PHC_Age_Cognition        | num     |   479 | DA DECIDERE
#     PHC_Diagnosis            | num     |     3 | DA DECIDERE
#     PHC_Sex                  | num     |     2 | DA DECIDERE
#     PHC_Race                 | num     |     5 | DA DECIDERE
#     PHC_Ethnicity            | num     |     2 | DA DECIDERE
#     PHC_Education            | num     |    15 | DA DECIDERE
#     AB42_RAW                 | num     |   185 | DA DECIDERE
#     PHC_AB42                 | num     |   185 | DA DECIDERE
#     Tau_RAW                  | num     |   341 | DA DECIDERE
#     PHC_Tau                  | num     |   341 | DA DECIDERE
#     pTau_RAW                 | num     |   339 | DA DECIDERE
#     PHC_pTau                 | num     |   339 | DA DECIDERE
#     AT_class                 | cat/str |     4 | DA DECIDERE
#     Platform                 | cat/str |     1 | DA DECIDERE
#     PHC_SCeNS_AB42_Score     | num     |   185 | DA DECIDERE
#     PHC_SCeNS_pTau_Score     | num     |   338 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
ADSP_PHC_BIOMARKER = DatasetConfig(
    file_code="ADSP_PHC_BIOMARKER",                          # <-- VERIFICA
    source="ADSP_PHC_BIOMARKER_25Jul2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="DRAWDATE",          # preferenza ADNI (alt: ['update_stamp']) VERIFICA
    # 19 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['SUBJID', 'PHC_Visit', 'PHC_Age_Biomarker', 'PHC_Age_Cognition', 'PHC_Diagnosis', 'PHC_Sex', 'PHC_Race', 'PHC_Ethnicity', 'PHC_Education', 'AB42_RAW', 'PHC_AB42', 'Tau_RAW', 'PHC_Tau', 'pTau_RAW', 'PHC_pTau', 'AT_class', 'Platform', 'PHC_SCeNS_AB42_Score', 'PHC_SCeNS_pTau_Score']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# AMPRION_ASYN_SAA
#   source: AMPRION_ASYN_SAA_11Aug2025.csv   |   righe campionate: 500   |   colonne: 9
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   481 | cand. ID
#     EXAMDATE                 | date    |   432 | cand. DATA
#     VISCODE2                 | cat/str |    23 | cand. VISITA
#     Sample_ID                | cat/str |   500 | cand. ID
#     Order                    | num     |   500 | DA DECIDERE
#     Amprion_ID               | cat/str |   500 | cand. ID
#     Result                   | cat/str |     4 | DA DECIDERE
#     Specimen_Color           | cat/str |     3 | DA DECIDERE
#     update_stamp             | date    |     8 | cand. DATA
# ------------------------------------------------------------------------
AMPRION_ASYN_SAA = DatasetConfig(
    file_code="AMPRION_ASYN_SAA",                          # <-- VERIFICA
    source="AMPRION_ASYN_SAA_11Aug2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['Sample_ID', 'Amprion_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['update_stamp']) VERIFICA
    viscode_reference="VISCODE2",
    # 3 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['Order', 'Result', 'Specimen_Color']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# AMYREAD
#   source: AMYREAD_28Oct2025.csv   |   righe campionate: 500   |   colonne: 23
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   500 | cand. ID
#     RID                      | num     |   500 | cand. ID
#     VISCODE                  | cat/str |     3 | cand. VISITA
#     VISCODE2                 | cat/str |    28 | cand. VISITA
#     SCANDATE                 | date    |   224 | cand. DATA
#     TRACERTYPE               | num     |     3 | DA DECIDERE
#     READDATE                 | date    |   131 | cand. DATA
#     OUTCOME                  | num     |     2 | DA DECIDERE
#     CORTREGION               | cat/str |    20 | DA DECIDERE
#     CONSENS                  | num     |     2 | DA DECIDERE
#     CONGRU                   | num     |     2 | DA DECIDERE
#     CONSRSN                  | num     |     2 | DA DECIDERE
#     CONSENSDATE              | date    |    33 | cand. DATA
#     CONSENSRES               | num     |     2 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   139 | cand. DATA
#     USERDATE2                | date    |   144 | cand. DATA
#     update_stamp             | date    |   138 | cand. DATA
# ------------------------------------------------------------------------
AMYREAD = DatasetConfig(
    file_code="AMYREAD",                          # <-- VERIFICA
    source="AMYREAD_28Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="SCANDATE",          # preferenza ADNI (alt: ['READDATE', 'CONSENSDATE', 'USERDATE', 'USERDATE2', 'update_stamp']) VERIFICA
    # 7 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['TRACERTYPE', 'OUTCOME', 'CORTREGION', 'CONSENS', 'CONGRU', 'CONSRSN', 'CONSENSRES']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# APOERES
#   source: APOERES_11Aug2025.csv   |   righe campionate: 500   |   colonne: 16
#   INDIZIO categoria dal nome (NON deciso): ['cofactor']
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   500 | cand. ID
#     RID                      | num     |   500 | cand. ID
#     VISCODE                  | cat/str |     2 | cand. VISITA
#     GENOTYPE                 | cat/str |     6 | DA DECIDERE
#     APTESTDT                 | date    |    41 | cand. DATA
#     APVOLUME                 | num     |    49 | DA DECIDERE
#     APRECEIVE                | num     |     2 | DA DECIDERE
#     APAMBTEMP                | num     |     1 | DA DECIDERE
#     APRESAMP                 | num     |     1 | DA DECIDERE
#     APUSABLE                 | num     |     1 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |    52 | cand. DATA
#     USERDATE2                | vuota   |     0 | DA DECIDERE
#     update_stamp             | date    |    52 | cand. DATA
# ------------------------------------------------------------------------
APOERES = DatasetConfig(
    file_code="APOERES",                          # <-- VERIFICA
    source="APOERES_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['cofactor'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['APTESTDT', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 7 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['GENOTYPE', 'APVOLUME', 'APRECEIVE', 'APAMBTEMP', 'APRESAMP', 'APUSABLE', 'USERDATE2']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# BAIPETNMRCFTP_08_17_22
#   source: BAIPETNMRCFTP_08_17_22_11Aug2025.csv   |   righe campionate: 500   |   colonne: 14
#   INDIZIO categoria dal nome (NON deciso): ['pet']
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     ORIGPROT                 | cat/str |     4 | DA DECIDERE
#     COLPROT                  | cat/str |     2 | DA DECIDERE
#     RID                      | num     |   288 | cand. ID
#     VISCODE                  | cat/str |    13 | cand. VISITA
#     VISCODE2                 | cat/str |    28 | cand. VISITA
#     EXAMDATE                 | date    |   375 | cand. DATA
#     RUNDATE                  | date    |     1 | cand. DATA
#     MODALITY                 | cat/str |     1 | DA DECIDERE
#     ENTORHINAL_SUVR          | num     |   474 | DA DECIDERE
#     INFERIOR_TEMPORAL_SUVR   | num     |   476 | DA DECIDERE
#     TAU_METAROI              | num     |   472 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
BAIPETNMRCFTP_08_17_22 = DatasetConfig(
    file_code="BAIPETNMRCFTP_08_17_22",                          # <-- VERIFICA
    source="BAIPETNMRCFTP_08_17_22_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['pet'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    # 6 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['ORIGPROT', 'COLPROT', 'MODALITY', 'ENTORHINAL_SUVR', 'INFERIOR_TEMPORAL_SUVR', 'TAU_METAROI']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# BHR_SP_FAQ
#   source: BHR_SP_FAQ_28Oct2025.csv   |   righe campionate: 35   |   colonne: 18
#   INDIZIO categoria dal nome (NON deciso): ['scale']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     AboutRID                 | num     |    28 | DA DECIDERE
#     StudyPartnerID           | num     |    28 | DA DECIDERE
#     AboutPTID                | cat/str |    28 | DA DECIDERE
#     Timepoint                | cat/str |     4 | DA DECIDERE
#     CollectedDateTime        | date    |    35 | cand. DATA
#     CollectedDate_DRVD       | date    |    31 | cand. DATA
#     latest                   | num     |     2 | DA DECIDERE
#     QID3_1                   | num     |     2 | DA DECIDERE
#     QID3_2                   | num     |     3 | DA DECIDERE
#     QID3_3                   | num     |     2 | DA DECIDERE
#     QID3_4                   | num     |     3 | DA DECIDERE
#     QID3_5                   | num     |     1 | DA DECIDERE
#     QID4_1                   | num     |     2 | DA DECIDERE
#     QID4_2                   | num     |     1 | DA DECIDERE
#     QID4_3                   | num     |     1 | DA DECIDERE
#     QID4_4                   | num     |     2 | DA DECIDERE
#     QID4_5                   | num     |     3 | DA DECIDERE
#     update_stamp             | date    |    10 | cand. DATA
# ------------------------------------------------------------------------
BHR_SP_FAQ = DatasetConfig(
    file_code="BHR_SP_FAQ",                          # <-- VERIFICA
    source="BHR_SP_FAQ_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['scale'])
    # id_column=?  candidati: NESSUNO  <-- DECIDI
    # date_column=?  candidati (dai valori): ['CollectedDateTime', 'CollectedDate_DRVD', 'update_stamp']  <-- DECIDI
    # 15 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['AboutRID', 'StudyPartnerID', 'AboutPTID', 'Timepoint', 'latest', 'QID3_1', 'QID3_2', 'QID3_3', 'QID3_4', 'QID3_5', 'QID4_1', 'QID4_2', 'QID4_3', 'QID4_4', 'QID4_5']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# BLCHANGE
#   source: BLCHANGE_25Jul2025.csv   |   righe campionate: 500   |   colonne: 29
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   405 | cand. ID
#     RID                      | num     |   405 | cand. ID
#     VISCODE                  | cat/str |     3 | cand. VISITA
#     VISCODE2                 | cat/str |     3 | cand. VISITA
#     EXAMDATE                 | date    |   193 | cand. DATA
#     BCPREDX                  | num     |     4 | DA DECIDERE
#     BCADAS                   | num     |     3 | DA DECIDERE
#     BCMMSE                   | num     |     3 | DA DECIDERE
#     BCMMSREC                 | num     |     3 | DA DECIDERE
#     BCNMMMS                  | num     |     3 | DA DECIDERE
#     BCNEUPSY                 | num     |     3 | DA DECIDERE
#     BCNONMEM                 | num     |     3 | DA DECIDERE
#     BCFAQ                    | num     |     3 | DA DECIDERE
#     BCCDR                    | num     |     3 | DA DECIDERE
#     BCDEPRES                 | num     |     3 | DA DECIDERE
#     BCSTROKE                 | num     |     2 | DA DECIDERE
#     BCDELIR                  | num     |     2 | DA DECIDERE
#     BCEXTCIR                 | num     |     3 | DA DECIDERE
#     BCCORADL                 | num     |     4 | DA DECIDERE
#     BCCORCOG                 | num     |     4 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   171 | cand. DATA
#     USERDATE2                | date    |     2 | cand. DATA
#     update_stamp             | date    |   172 | cand. DATA
# ------------------------------------------------------------------------
BLCHANGE = DatasetConfig(
    file_code="BLCHANGE",                          # <-- VERIFICA
    source="BLCHANGE_25Jul2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['USERDATE', 'USERDATE2', 'update_stamp']) VERIFICA
    # 15 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['BCPREDX', 'BCADAS', 'BCMMSE', 'BCMMSREC', 'BCNMMMS', 'BCNEUPSY', 'BCNONMEM', 'BCFAQ', 'BCCDR', 'BCDEPRES', 'BCSTROKE', 'BCDELIR', 'BCEXTCIR', 'BCCORADL', 'BCCORCOG']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# BLENNOWCSFNFL
#   source: BLENNOWCSFNFL_11Aug2025.csv   |   righe campionate: 415   |   colonne: 8
#   INDIZIO categoria dal nome (NON deciso): ['plasma', 'csf']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   399 | cand. ID
#     VISCODE                  | cat/str |     1 | cand. VISITA
#     USERDATE                 | date    |     1 | cand. DATA
#     EXAMDATE                 | date    |   243 | cand. DATA
#     VOLUME                   | cat/str |     1 | DA DECIDERE
#     CSFNFL                   | num     |   358 | DA DECIDERE
#     COMMENTS                 | cat/str |     2 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
BLENNOWCSFNFL = DatasetConfig(
    file_code="BLENNOWCSFNFL",                          # <-- VERIFICA
    source="BLENNOWCSFNFL_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma', 'csf'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['USERDATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 3 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['VOLUME', 'CSFNFL', 'COMMENTS']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# BLENNOWPLASMATAU
#   source: BLENNOWPLASMATAU_11Aug2025.csv   |   righe campionate: 500   |   colonne: 8
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 1 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   500 | cand. ID
#     VISCODE                  | cat/str |     1 | cand. VISITA
#     USERDATE                 | date    |     1 | cand. DATA
#     EXAMDATE                 | date    |   244 | cand. DATA
#     VOL                      | cat/str |     1 | DA DECIDERE
#     PLASMATAU                | num     |   304 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
BLENNOWPLASMATAU = DatasetConfig(
    file_code="BLENNOWPLASMATAU",                          # <-- VERIFICA
    source="BLENNOWPLASMATAU_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['USERDATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 2 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['VOL', 'PLASMATAU']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# C2N_PRECIVITYAD2_PLASMA
#   source: C2N_PRECIVITYAD2_PLASMA_11Aug2025.csv   |   righe campionate: 500   |   colonne: 18
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 4 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   446 | cand. ID
#     RID                      | num     |   446 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     VISCODE2                 | cat/str |    29 | cand. VISITA
#     EXAMDATE                 | date    |   229 | cand. DATA
#     pT217_C2N                | num     |   261 | DA DECIDERE
#     npT217_C2N               | num     |   490 | DA DECIDERE
#     AB42_C2N                 | num     |   492 | DA DECIDERE
#     AB40_C2N                 | num     |   495 | DA DECIDERE
#     AB42_AB40_C2N            | num     |    65 | DA DECIDERE
#     pT217_npT217_C2N         | num     |   338 | DA DECIDERE
#     APS2_C2N                 | num     |    96 | DA DECIDERE
#     APOE_C2N                 | cat/str |     6 | DA DECIDERE
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
C2N_PRECIVITYAD2_PLASMA = DatasetConfig(
    file_code="C2N_PRECIVITYAD2_PLASMA",                          # <-- VERIFICA
    source="C2N_PRECIVITYAD2_PLASMA_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['update_stamp']) VERIFICA
    # 8 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['pT217_C2N', 'npT217_C2N', 'AB42_C2N', 'AB40_C2N', 'AB42_AB40_C2N', 'pT217_npT217_C2N', 'APS2_C2N', 'APOE_C2N']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# CDR
#   source: CDR_28Oct2025.csv   |   righe campionate: 500   |   colonne: 25
#   INDIZIO categoria dal nome (NON deciso): ['scale']
#   ignorate 6 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   481 | cand. ID
#     RID                      | num     |   481 | cand. ID
#     VISCODE                  | cat/str |     3 | cand. VISITA
#     VISCODE2                 | cat/str |     3 | cand. VISITA
#     VISDATE                  | date    |   165 | cand. DATA
#     CDSOURCE                 | num     |     2 | DA DECIDERE
#     SPID                     | vuota   |     0 | DA DECIDERE
#     CDMEMORY                 | num     |     4 | DA DECIDERE
#     CDORIENT                 | num     |     4 | DA DECIDERE
#     CDJUDGE                  | num     |     4 | DA DECIDERE
#     CDCOMMUN                 | num     |     4 | DA DECIDERE
#     CDHOME                   | num     |     4 | DA DECIDERE
#     CDCARE                   | num     |     4 | DA DECIDERE
#     CDGLOBAL                 | num     |     4 | DA DECIDERE
#     CDRSB                    | num     |    17 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   161 | cand. DATA
#     USERDATE2                | date    |     1 | cand. DATA
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
CDR = DatasetConfig(
    file_code="CDR",                          # <-- VERIFICA
    source="CDR_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['scale'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['VISDATE', 'USERDATE2', 'update_stamp']) VERIFICA
    # 10 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['CDSOURCE', 'SPID', 'CDMEMORY', 'CDORIENT', 'CDJUDGE', 'CDCOMMUN', 'CDHOME', 'CDCARE', 'CDGLOBAL', 'CDRSB']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# CSFALPHASYN_03_21_14
#   source: CSFALPHASYN_03_21_14_11Aug2025.csv   |   righe campionate: 389   |   colonne: 9
#   INDIZIO categoria dal nome (NON deciso): ['csf']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   389 | cand. ID
#     EXAMDATE                 | date    |   237 | cand. DATA
#     PROTOCOL                 | cat/str |     1 | DA DECIDERE
#     BOX                      | cat/str |     5 | DA DECIDERE
#     LUMINEX_BATCH_NUMBER     | num     |     5 | DA DECIDERE
#     LUMINEX_TESTING_DATE     | date    |     3 | cand. DATA
#     ALPHA_SYN                | num     |   125 | DA DECIDERE
#     HEMOGLOBIN               | num     |   232 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
CSFALPHASYN_03_21_14 = DatasetConfig(
    file_code="CSFALPHASYN_03_21_14",                          # <-- VERIFICA
    source="CSFALPHASYN_03_21_14_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['LUMINEX_TESTING_DATE', 'update_stamp']) VERIFICA
    # 5 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['PROTOCOL', 'BOX', 'LUMINEX_BATCH_NUMBER', 'ALPHA_SYN', 'HEMOGLOBIN']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# DXSUM
#   source: DXSUM_25Jul2025.csv   |   righe campionate: 500   |   colonne: 41
#   INDIZIO categoria dal nome (NON deciso): ['cofactor']
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   405 | cand. ID
#     RID                      | num     |   405 | cand. ID
#     VISCODE                  | cat/str |     3 | cand. VISITA
#     VISCODE2                 | cat/str |     3 | cand. VISITA
#     EXAMDATE                 | date    |   192 | cand. DATA
#     DIAGNOSIS                | num     |     3 | DA DECIDERE
#     DXNORM                   | num     |     2 | DA DECIDERE
#     DXNODEP                  | num     |     2 | DA DECIDERE
#     DXMCI                    | num     |     2 | DA DECIDERE
#     DXMDES                   | num     |     3 | DA DECIDERE
#     DXMPTR1                  | num     |     3 | DA DECIDERE
#     DXMPTR2                  | num     |     3 | DA DECIDERE
#     DXMPTR3                  | num     |     4 | DA DECIDERE
#     DXMPTR4                  | num     |     4 | DA DECIDERE
#     DXMPTR5                  | num     |     3 | DA DECIDERE
#     DXMPTR6                  | num     |     3 | DA DECIDERE
#     DXMDUE                   | num     |     3 | DA DECIDERE
#     DXMOTHET                 | num     |     3 | DA DECIDERE
#     DXDSEV                   | num     |     3 | DA DECIDERE
#     DXDDUE                   | vuota   |     0 | DA DECIDERE
#     DXAD                     | num     |     2 | DA DECIDERE
#     DXAPP                    | num     |     3 | DA DECIDERE
#     DXAPROB                  | num     |     4 | DA DECIDERE
#     DXAPOSS                  | num     |     2 | DA DECIDERE
#     DXPARK                   | num     |     1 | DA DECIDERE
#     DXPDES                   | num     |     1 | DA DECIDERE
#     DXPCOG                   | num     |     1 | DA DECIDERE
#     DXPATYP                  | num     |     1 | DA DECIDERE
#     DXDEP                    | vuota   |     0 | DA DECIDERE
#     DXOTHDEM                 | num     |     1 | DA DECIDERE
#     DXODES                   | num     |     1 | DA DECIDERE
#     DXCONFID                 | num     |     4 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   179 | cand. DATA
#     USERDATE2                | date    |     2 | cand. DATA
#     update_stamp             | date    |   181 | cand. DATA
# ------------------------------------------------------------------------
DXSUM = DatasetConfig(
    file_code="DXSUM",                          # <-- VERIFICA
    source="DXSUM_25Jul2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['cofactor'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['USERDATE', 'USERDATE2', 'update_stamp']) VERIFICA
    # 27 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['DIAGNOSIS', 'DXNORM', 'DXNODEP', 'DXMCI', 'DXMDES', 'DXMPTR1', 'DXMPTR2', 'DXMPTR3', 'DXMPTR4', 'DXMPTR5', 'DXMPTR6', 'DXMDUE', 'DXMOTHET', 'DXDSEV', 'DXDDUE', 'DXAD', 'DXAPP', 'DXAPROB', 'DXAPOSS', 'DXPARK', 'DXPDES', 'DXPCOG', 'DXPATYP', 'DXDEP', 'DXOTHDEM', 'DXODES', 'DXCONFID']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# FAQ
#   source: FAQ_28Oct2025.csv   |   righe campionate: 500   |   colonne: 27
#   INDIZIO categoria dal nome (NON deciso): ['scale']
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   401 | cand. ID
#     RID                      | num     |   401 | cand. ID
#     VISCODE                  | cat/str |     2 | cand. VISITA
#     VISCODE2                 | cat/str |     2 | cand. VISITA
#     VISDATE                  | date    |   186 | cand. DATA
#     SOURCE                   | num     |     3 | DA DECIDERE
#     FAQFINAN                 | num     |     7 | DA DECIDERE
#     FAQFORM                  | num     |     7 | DA DECIDERE
#     FAQSHOP                  | num     |     7 | DA DECIDERE
#     FAQGAME                  | num     |     7 | DA DECIDERE
#     FAQBEVG                  | num     |     7 | DA DECIDERE
#     FAQMEAL                  | num     |     7 | DA DECIDERE
#     FAQEVENT                 | num     |     7 | DA DECIDERE
#     FAQTV                    | num     |     6 | DA DECIDERE
#     FAQREM                   | num     |     7 | DA DECIDERE
#     FAQTRAVL                 | num     |     6 | DA DECIDERE
#     FAQTOTAL                 | num     |    31 | DA DECIDERE
#     SPID                     | vuota   |     0 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   179 | cand. DATA
#     USERDATE2                | vuota   |     0 | DA DECIDERE
#     update_stamp             | date    |   179 | cand. DATA
# ------------------------------------------------------------------------
FAQ = DatasetConfig(
    file_code="FAQ",                          # <-- VERIFICA
    source="FAQ_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['scale'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['VISDATE', 'update_stamp']) VERIFICA
    # 14 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['SOURCE', 'FAQFINAN', 'FAQFORM', 'FAQSHOP', 'FAQGAME', 'FAQBEVG', 'FAQMEAL', 'FAQEVENT', 'FAQTV', 'FAQREM', 'FAQTRAVL', 'FAQTOTAL', 'SPID', 'USERDATE2']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# FNIH_PLASMA_PTAU_PROJECT
#   source: FNIH_PLASMA_PTAU_PROJECT_11Aug2025.csv   |   righe campionate: 500   |   colonne: 14
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PROT                     | cat/str |     3 | DA DECIDERE
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     5 | cand. VISITA
#     VISCODE2                 | cat/str |    12 | cand. VISITA
#     EXAMDATE                 | date    |    99 | cand. DATA
#     TYPE                     | cat/str |     1 | DA DECIDERE
#     SAMPLEID                 | cat/str |   500 | DA DECIDERE
#     PTAU_181                 | num     |   350 | DA DECIDERE
#     PTAU_231                 | vuota   |     0 | DA DECIDERE
#     UNITS                    | cat/str |     1 | DA DECIDERE
#     RUN_NUM                  | vuota   |     0 | DA DECIDERE
#     RUNDATE                  | date    |     5 | cand. DATA
#     IMMUNOASSAY              | cat/str |     4 | DA DECIDERE
#     update_stamp             | date    |     4 | cand. DATA
# ------------------------------------------------------------------------
FNIH_PLASMA_PTAU_PROJECT = DatasetConfig(
    file_code="FNIH_PLASMA_PTAU_PROJECT",                          # <-- VERIFICA
    source="FNIH_PLASMA_PTAU_PROJECT_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    # 8 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['PROT', 'TYPE', 'SAMPLEID', 'PTAU_181', 'PTAU_231', 'UNITS', 'RUN_NUM', 'IMMUNOASSAY']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# FUJIREBIOABETA
#   source: FUJIREBIOABETA_11Aug2025.csv   |   righe campionate: 442   |   colonne: 19
#   INDIZIO categoria dal nome (NON deciso): ['csf']
#   ignorate 4 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   423 | cand. ID
#     VISCODE                  | cat/str |     9 | cand. VISITA
#     VISCODE2                 | cat/str |     7 | cand. VISITA
#     EXAMDATE                 | date    |   325 | cand. DATA
#     DRAWDTE                  | date    |   325 | cand. DATA
#     SITE                     | cat/str |    57 | DA DECIDERE
#     VOL                      | num     |     4 | DA DECIDERE
#     RECDTE                   | date    |   303 | cand. DATA
#     STORDTE                  | date    |   177 | cand. DATA
#     RUNDATE                  | date    |     3 | cand. DATA
#     ABETA42                  | num     |   370 | DA DECIDERE
#     ABETA40                  | num     |   433 | DA DECIDERE
#     ABETA42_40               | num     |    84 | DA DECIDERE
#     COMMENTS                 | cat/str |     1 | DA DECIDERE
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
FUJIREBIOABETA = DatasetConfig(
    file_code="FUJIREBIOABETA",                          # <-- VERIFICA
    source="FUJIREBIOABETA_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWDTE', 'RECDTE', 'STORDTE', 'RUNDATE', 'update_stamp']) VERIFICA
    # 6 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['SITE', 'VOL', 'ABETA42', 'ABETA40', 'ABETA42_40', 'COMMENTS']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# ITEM
#   source: ITEM.csv   |   righe campionate: 500   |   colonne: 766
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |    71 | cand. ID
#     VISCODE                  | cat/str |     7 | cand. VISITA
#     ADAS_QuestionnaireNotAttempted | num     |     1 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W1_butter | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W2_arm    | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W3_shore  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W4_letter | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W5_queen  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W6_cabin  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W7_pole   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W8_ticket | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W9_grass  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL1_W10_engine | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W1_pole   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W2_letter | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W3_butter | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W4_queen  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W5_arm    | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W6_shore  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W7_grass  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W8_cabin  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W9_ticket | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL1_W10_engine | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W1_shore  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W2_letter | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W3_arm    | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W4_cabin  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W5_pole   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W6_ticket | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W7_engine | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W8_grass  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W9_butter | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL1_W10_queen | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W1_bottle | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W2_potato | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W3_girl   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W4_temple | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W5_star   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W6_animal | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W7_forest | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W8_lake   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W9_clock  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL2_W10_office | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W1_forest | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W2_temple | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W3_bottle | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W4_star   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W5_potato | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W6_girl   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W7_clock  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W8_animal | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W9_lake   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL2_W10_office | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W1_girl   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W2_temple | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W3_potato | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W4_animal | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W5_forest | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W6_lake   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W7_office | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W8_clock  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W9_bottle | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL2_W10_star  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W1_coast  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W2_doll   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W3_lip    | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W4_chair  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W5_student | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W6_apple  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W7_horse  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W8_pipe   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W9_valley | num     |     2 | DA DECIDERE
#     ADAS_Q1_T1_WL3_W10_rock  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W1_horse  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W2_chair  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W3_coast  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W4_student | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W5_doll   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W6_lip    | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W7_valley | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W8_apple  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W9_pipe   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T2_WL3_W10_rock  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W1_lip    | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W2_chair  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W3_doll   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W4_apple  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W5_horse  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W6_pipe   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W7_rock   | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W8_valley | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W9_coast  | num     |     2 | DA DECIDERE
#     ADAS_Q1_T3_WL3_W10_student | num     |     2 | DA DECIDERE
#     ADAS_Q1_TimeEnded        | num     |   177 | DA DECIDERE
#     ADAS_Q2a                 | num     |     2 | DA DECIDERE
#     ADAS_Q2b                 | num     |     2 | DA DECIDERE
#     ADAS_Q2c                 | num     |     2 | DA DECIDERE
#     ADAS_Q2d                 | num     |     2 | DA DECIDERE
#     ADAS_Q2e                 | num     |     2 | DA DECIDERE
#     ADAS_Q3a                 | num     |     2 | DA DECIDERE
#     ADAS_Q3b                 | num     |     2 | DA DECIDERE
#     ADAS_Q3c                 | num     |     2 | DA DECIDERE
#     ADAS_Q3d                 | num     |     2 | DA DECIDERE
#     ADAS_Q4_TimeBegan        | num     |   193 | DA DECIDERE
#     ADAS_Q4_WL1_W1_butter    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W2_arm       | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W3_shore     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W4_letter    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W5_queen     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W6_cabin     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W7_pole      | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W8_ticket    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W9_grass     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL1_W10_engine   | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W1_bottle    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W2_potato    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W3_girl      | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W4_temple    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W5_star      | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W6_animal    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W7_forest    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W8_lake      | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W9_clock     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL2_W10_office   | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W1_coast     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W2_doll      | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W3_lip       | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W4_chair     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W5_student   | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W6_apple     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W7_horse     | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W8_pipe      | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W9_valley    | num     |     2 | DA DECIDERE
#     ADAS_Q4_WL3_W10_rock     | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Flower          | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Bed             | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Whistle         | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Pencil          | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Rattle          | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Mask            | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Scissors        | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Comb            | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Wallet          | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Harmonica       | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Stethoscope     | num     |     2 | DA DECIDERE
#     ADAS_Q5a_Tongs           | num     |     2 | DA DECIDERE
#     ADAS_Q5b_Thumb           | num     |     2 | DA DECIDERE
#     ADAS_Q5b_Middle          | num     |     2 | DA DECIDERE
#     ADAS_Q5b_Ring            | num     |     2 | DA DECIDERE
#     ADAS_Q5b_Index           | num     |     2 | DA DECIDERE
#     ADAS_Q5b_Pinky           | num     |     2 | DA DECIDERE
#     ADAS_Q6a                 | num     |     2 | DA DECIDERE
#     ADAS_Q6b                 | num     |     2 | DA DECIDERE
#     ADAS_Q6c                 | num     |     2 | DA DECIDERE
#     ADAS_Q6d                 | num     |     2 | DA DECIDERE
#     ADAS_Q6e                 | num     |     2 | DA DECIDERE
#     ADAS_Q7a                 | num     |     2 | DA DECIDERE
#     ADAS_Q7b                 | num     |     2 | DA DECIDERE
#     ADAS_Q7c                 | num     |     2 | DA DECIDERE
#     ADAS_Q7d                 | num     |     2 | DA DECIDERE
#     ADAS_Q7e                 | num     |     2 | DA DECIDERE
#     ADAS_Q7f                 | num     |     2 | DA DECIDERE
#     ADAS_Q7g                 | num     |     2 | DA DECIDERE
#     ADAS_Q7h                 | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W1_nurse | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W2_magazine | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W3_wizard | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W4_van   | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W5_leopard | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W6_sale  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W7_sea   | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W8_train | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W9_coin  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W10_ship | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W11_institution | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W12_map  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W13_axe  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W14_board | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W15_carrot | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W16_milk | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W17_volume | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W18_forest | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W19_anchor | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W20_gem  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W21_cat  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W22_fund | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W23_edge | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_REC_W24_cake | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W1_nurse | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W2_magazine | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W3_wizard | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W4_van | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W5_leopard | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W6_sale | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W7_sea | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W8_train | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W9_coin | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W10_ship | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W11_institution | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W12_map | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W13_axe | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W14_board | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W15_carrot | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W16_milk | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W17_volume | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W18_forest | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W19_anchor | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W20_gem | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W21_cat | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W22_fund | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W23_edge | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL1_Reminder_W24_cake | num     |     1 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W1_cost  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W2_nation | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W3_chimney | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W4_sparrow | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W5_damages | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W6_traffic | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W7_sandwich | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W8_service | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W9_shell | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W10_solution | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W11_yard | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W12_tube | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W13_body | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W14_ground | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W15_stick | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W16_engine | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W17_riches | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W18_gravity | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W19_summer | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W20_wisdom | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W21_man  | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W22_meal | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W23_passenger | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_REC_W24_acid | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W1_cost | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W2_nation | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W3_chimney | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W4_sparrow | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W5_damages | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W6_traffic | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W7_sandwich | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W8_service | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W9_shell | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W10_solution | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W11_yard | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W12_tube | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W13_body | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W14_ground | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W15_stick | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W16_engine | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W17_riches | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W18_gravity | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W19_summer | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W20_wisdom | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W21_man | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W22_meal | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W23_passenger | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL2_Reminder_W24_acid | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W1_silence | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W2_elbow | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W3_daughter | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W4_powder | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W5_canal | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W6_forehead | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W7_tiger | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W8_twilight | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W9_dragon | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W10_chamber | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W11_sister | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W12_beggar | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W13_echo | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W14_nephew | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W15_duty | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W16_village | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W17_corner | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W18_olive | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W19_music | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W20_courage | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W21_bushel | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W22_ribbon | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W23_object | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_REC_W24_collar | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W1_silence | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W2_elbow | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W3_daughter | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W4_powder | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W5_canal | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W6_forehead | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W7_tiger | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W8_twilight | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W9_dragon | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W10_chamber | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W11_sister | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W12_beggar | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W13_echo | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W14_nephew | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W15_duty | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W16_village | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W17_corner | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W18_olive | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W19_music | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W20_courage | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W21_bushel | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W22_ribbon | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W23_object | num     |     2 | DA DECIDERE
#     ADAS_Q8_WL3_Reminder_W24_collar | num     |     2 | DA DECIDERE
#     ADAS_Q9                  | num     |     6 | DA DECIDERE
#     ADAS_Q10                 | num     |     5 | DA DECIDERE
#     ADAS_Q11                 | num     |     6 | DA DECIDERE
#     ADAS_Q12                 | num     |     6 | DA DECIDERE
#     ADAS_Q13a                | num     |    40 | DA DECIDERE
#     ADAS_Q13b                | num     |     6 | DA DECIDERE
#     ADAS_Q13c                | num     |     7 | DA DECIDERE
#     ADAS_ExamDate            | cat/str |   251 | DA DECIDERE
#     ANART_QuestionnaireNotAttempted | num     |     1 | DA DECIDERE
#     ANART_Q1                 | num     |     2 | DA DECIDERE
#     ANART_Q2                 | num     |     2 | DA DECIDERE
#     ANART_Q3                 | num     |     2 | DA DECIDERE
#     ANART_Q4                 | num     |     2 | DA DECIDERE
#     ANART_Q5                 | num     |     2 | DA DECIDERE
#     ANART_Q6                 | num     |     2 | DA DECIDERE
#     ANART_Q7                 | num     |     2 | DA DECIDERE
#     ANART_Q8                 | num     |     2 | DA DECIDERE
#     ANART_Q9                 | num     |     2 | DA DECIDERE
#     ANART_Q10                | num     |     2 | DA DECIDERE
#     ANART_Q11                | num     |     2 | DA DECIDERE
#     ANART_Q12                | num     |     2 | DA DECIDERE
#     ANART_Q13                | num     |     2 | DA DECIDERE
#     ANART_Q14                | num     |     2 | DA DECIDERE
#     ANART_Q15                | num     |     2 | DA DECIDERE
#     ANART_Q16                | num     |     2 | DA DECIDERE
#     ANART_Q17                | num     |     2 | DA DECIDERE
#     ANART_Q18                | num     |     2 | DA DECIDERE
#     ANART_Q19                | num     |     2 | DA DECIDERE
#     ANART_Q20                | num     |     2 | DA DECIDERE
#     ANART_Q21                | num     |     2 | DA DECIDERE
#     ANART_Q22                | num     |     2 | DA DECIDERE
#     ANART_Q23                | num     |     2 | DA DECIDERE
#     ANART_Q24                | num     |     2 | DA DECIDERE
#     ANART_Q25                | num     |     2 | DA DECIDERE
#     ANART_Q26                | num     |     2 | DA DECIDERE
#     ANART_Q27                | num     |     2 | DA DECIDERE
#     ANART_Q28                | num     |     2 | DA DECIDERE
#     ANART_Q29                | num     |     2 | DA DECIDERE
#     ANART_Q30                | num     |     2 | DA DECIDERE
#     ANART_Q31                | num     |     2 | DA DECIDERE
#     ANART_Q32                | num     |     2 | DA DECIDERE
#     ANART_Q33                | num     |     2 | DA DECIDERE
#     ANART_Q34                | num     |     2 | DA DECIDERE
#     ANART_Q35                | num     |     2 | DA DECIDERE
#     ANART_Q36                | num     |     2 | DA DECIDERE
#     ANART_Q37                | num     |     2 | DA DECIDERE
#     ANART_Q38                | num     |     2 | DA DECIDERE
#     ANART_Q39                | num     |     2 | DA DECIDERE
#     ANART_Q40                | num     |     2 | DA DECIDERE
#     ANART_Q41                | num     |     2 | DA DECIDERE
#     ANART_Q42                | num     |     2 | DA DECIDERE
#     ANART_Q43                | num     |     2 | DA DECIDERE
#     ANART_Q44                | num     |     2 | DA DECIDERE
#     ANART_Q45                | num     |     2 | DA DECIDERE
#     ANART_Q46                | num     |     2 | DA DECIDERE
#     ANART_Q47                | num     |     2 | DA DECIDERE
#     ANART_Q48                | num     |     2 | DA DECIDERE
#     ANART_Q49                | num     |     2 | DA DECIDERE
#     ANART_Q50                | num     |     2 | DA DECIDERE
#     ANART_ExamDate           | cat/str |    52 | DA DECIDERE
#     AVLT_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     AVLT_StartTime           | num     |   187 | DA DECIDERE
#     AVLTA_WL1a_T1_W1_drum    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W2_curtain | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W3_bell    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W4_coffee  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W5_school  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W6_parent  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W7_moon    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W8_garden  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W9_hat     | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W10_farmer | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W11_nose   | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W12_turkey | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W13_color  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W14_house  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T1_W15_river  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W1_drum    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W2_curtain | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W3_bell    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W4_coffee  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W5_school  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W6_parent  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W7_moon    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W8_garden  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W9_hat     | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W10_farmer | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W11_nose   | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W12_turkey | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W13_color  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W14_house  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T2_W15_river  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W1_drum    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W2_curtain | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W3_bell    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W4_coffee  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W5_school  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W6_parent  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W7_moon    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W8_garden  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W9_hat     | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W10_farmer | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W11_nose   | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W12_turkey | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W13_color  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W14_house  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T3_W15_river  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W1_drum    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W2_curtain | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W3_bell    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W4_coffee  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W5_school  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W6_parent  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W7_moon    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W8_garden  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W9_hat     | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W10_farmer | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W11_nose   | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W12_turkey | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W13_color  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W14_house  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T4_W15_river  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W1_drum    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W2_curtain | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W3_bell    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W4_coffee  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W5_school  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W6_parent  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W7_moon    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W8_garden  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W9_hat     | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W10_farmer | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W11_nose   | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W12_turkey | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W13_color  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W14_house  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T5_W15_river  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W1_drum    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W2_curtain | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W3_bell    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W4_coffee  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W5_school  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W6_parent  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W7_moon    | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W8_garden  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W9_hat     | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W10_farmer | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W11_nose   | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W12_turkey | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W13_color  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W14_house  | num     |     2 | DA DECIDERE
#     AVLTA_WL1a_T6_W15_river  | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W1_desk    | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W2_ranger  | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W3_bird    | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W4_shoe    | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W5_stove   | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W6_mountain | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W7_glasses | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W8_towel   | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W9_cloud   | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W10_boat   | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W11_lamb   | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W12_gun    | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W13_pencil | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W14_church | num     |     2 | DA DECIDERE
#     AVLTA_WL1b_T7_W15_fish   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W1_doll    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W2_mirror  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W3_nail    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W4_sailor  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W5_heart   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W6_desert  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W7_face    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W8_letter  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W9_bed     | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W10_machine | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W11_milk   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W12_helmet | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W13_music  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W14_horse  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T1_W15_road   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W1_doll    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W2_mirror  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W3_nail    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W4_sailor  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W5_heart   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W6_desert  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W7_face    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W8_letter  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W9_bed     | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W10_machine | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W11_milk   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W12_helmet | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W13_music  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W14_horse  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T2_W15_road   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W1_doll    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W2_mirror  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W3_nail    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W4_sailor  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W5_heart   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W6_desert  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W7_face    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W8_letter  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W9_bed     | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W10_machine | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W11_milk   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W12_helmet | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W13_music  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W14_horse  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T3_W15_road   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W1_doll    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W2_mirror  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W3_nail    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W4_sailor  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W5_heart   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W6_desert  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W7_face    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W8_letter  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W9_bed     | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W10_machine | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W11_milk   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W12_helmet | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W13_music  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W14_horse  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T4_W15_road   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W1_doll    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W2_mirror  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W3_nail    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W4_sailor  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W5_heart   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W6_desert  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W7_face    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W8_letter  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W9_bed     | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W10_machine | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W11_milk   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W12_helmet | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W13_music  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W14_horse  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T5_W15_road   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W1_doll    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W2_mirror  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W3_nail    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W4_sailor  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W5_heart   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W6_desert  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W7_face    | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W8_letter  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W9_bed     | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W10_machine | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W11_milk   | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W12_helmet | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W13_music  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W14_horse  | num     |     2 | DA DECIDERE
#     AVLTB_WL2a_T6_W15_road   | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W1_dish    | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W2_jester  | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W3_hill    | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W4_coat    | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W5_tool    | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W6_forest  | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W7_water   | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W8_ladder  | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W9_girl    | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W10_foot   | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W11_shield | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W12_pie    | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W13_insect | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W14_ball   | num     |     2 | DA DECIDERE
#     AVLTB_WL2b_T7_W15_car    | num     |     2 | DA DECIDERE
#     AVLT_Trial1Int           | num     |     7 | DA DECIDERE
#     AVLT_Trial2Int           | num     |     8 | DA DECIDERE
#     AVLT_Trial3Int           | num     |     8 | DA DECIDERE
#     AVLT_Trial4Int           | num     |     8 | DA DECIDERE
#     AVLT_Trial5Int           | num     |     8 | DA DECIDERE
#     AVLT_Trial6Int           | num     |    10 | DA DECIDERE
#     AVLT_Trial7Int           | num     |    10 | DA DECIDERE
#     AVLT_ExamDate            | cat/str |   251 | DA DECIDERE
#     AVLT_Delay_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     AVLT_DelayTime           | num     |   189 | DA DECIDERE
#     AVLT_Delay_WL1_W1_drum   | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W2_curtain | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W3_bell   | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W4_coffee | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W5_school | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W6_parent | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W7_moon   | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W8_garden | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W9_hat    | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W10_farmer | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W11_nose  | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W12_turkey | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W13_color | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W14_house | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL1_W15_river | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W1_doll   | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W2_mirror | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W3_nail   | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W4_sailor | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W5_heart  | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W6_desert | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W7_face   | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W8_letter | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W9_bed    | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W10_machine | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W11_milk  | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W12_helmet | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W13_music | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W14_horse | num     |     2 | DA DECIDERE
#     AVLT_Delay_WL2_W15_road  | num     |     2 | DA DECIDERE
#     AVLT_Delay_Int           | num     |    11 | DA DECIDERE
#     AVLT_Delay_Rec           | num     |    16 | DA DECIDERE
#     AVLT_Delay_TotInt        | num     |    13 | DA DECIDERE
#     AVLT_Delay_ExamDate      | cat/str |   251 | DA DECIDERE
#     BosNam_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     BosNam_Q1                | num     |     3 | DA DECIDERE
#     BosNam_Q3                | num     |     2 | DA DECIDERE
#     BosNam_Q5                | num     |     4 | DA DECIDERE
#     BosNam_Q7                | num     |     3 | DA DECIDERE
#     BosNam_Q9                | num     |     4 | DA DECIDERE
#     BosNam_Q11               | num     |     5 | DA DECIDERE
#     BosNam_Q13               | num     |     4 | DA DECIDERE
#     BosNam_Q15               | num     |     3 | DA DECIDERE
#     BosNam_Q17               | num     |     4 | DA DECIDERE
#     BosNam_Q19               | num     |     5 | DA DECIDERE
#     BosNam_Q21               | num     |     4 | DA DECIDERE
#     BosNam_Q23               | num     |     5 | DA DECIDERE
#     BosNam_Q25               | num     |     4 | DA DECIDERE
#     BosNam_Q27               | num     |     4 | DA DECIDERE
#     BosNam_Q29               | num     |     5 | DA DECIDERE
#     BosNam_Q31               | num     |     6 | DA DECIDERE
#     BosNam_Q33               | num     |     4 | DA DECIDERE
#     BosNam_Q35               | num     |     4 | DA DECIDERE
#     BosNam_Q37               | num     |     6 | DA DECIDERE
#     BosNam_Q39               | num     |     4 | DA DECIDERE
#     BosNam_Q41               | num     |     4 | DA DECIDERE
#     BosNam_Q43               | num     |     5 | DA DECIDERE
#     BosNam_Q45               | num     |     5 | DA DECIDERE
#     BosNam_Q47               | num     |     5 | DA DECIDERE
#     BosNam_Q49               | num     |     4 | DA DECIDERE
#     BosNam_Q51               | num     |     5 | DA DECIDERE
#     BosNam_Q53               | num     |     5 | DA DECIDERE
#     BosNam_Q55               | num     |     6 | DA DECIDERE
#     BosNam_Q57               | num     |     6 | DA DECIDERE
#     BosNam_Q59               | num     |     6 | DA DECIDERE
#     BosNam_ExamDate          | cat/str |   253 | DA DECIDERE
#     CatFlu_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     CatFlu_Practise          | num     |     6 | DA DECIDERE
#     CatFlu_Animal_Total      | num     |    39 | DA DECIDERE
#     CatFlu_Animal_Perseverations | num     |    12 | DA DECIDERE
#     CatFlu_Animal_Intrusions | num     |     5 | DA DECIDERE
#     CatFlu_Vegetable_Total   | num     |    28 | DA DECIDERE
#     CatFlu_Vegetable_Perseverations | num     |     7 | DA DECIDERE
#     CatFlu_Vegetable_Intrusions | num     |    12 | DA DECIDERE
#     CatFlu_ExamDate          | cat/str |   253 | DA DECIDERE
#     CDT_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     CDT_Q1pt1                | num     |     2 | DA DECIDERE
#     CDT_Q1pt2                | num     |     2 | DA DECIDERE
#     CDT_Q1pt3                | num     |     2 | DA DECIDERE
#     CDT_Q1pt4                | num     |     2 | DA DECIDERE
#     CDT_Q1pt5                | num     |     2 | DA DECIDERE
#     CDT_Q2pt1                | num     |     2 | DA DECIDERE
#     CDT_Q2pt2                | num     |     2 | DA DECIDERE
#     CDT_Q2pt3                | num     |     2 | DA DECIDERE
#     CDT_Q2pt4                | num     |     2 | DA DECIDERE
#     CDT_Q2pt5                | num     |     2 | DA DECIDERE
#     CDT_ExamDate             | cat/str |   251 | DA DECIDERE
#     DSBac_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     DSBac_Q1a                | num     |     3 | DA DECIDERE
#     DSBac_Q1b                | num     |     3 | DA DECIDERE
#     DSBac_Q2a                | num     |     3 | DA DECIDERE
#     DSBac_Q2b                | num     |     3 | DA DECIDERE
#     DSBac_Q3a                | num     |     3 | DA DECIDERE
#     DSBac_Q3b                | num     |     3 | DA DECIDERE
#     DSBac_Q4a                | num     |     3 | DA DECIDERE
#     DSBac_Q4b                | num     |     3 | DA DECIDERE
#     DSBac_Q5a                | num     |     3 | DA DECIDERE
#     DSBac_Q5b                | num     |     3 | DA DECIDERE
#     DSBac_Q6a                | num     |     3 | DA DECIDERE
#     DSBac_Q6b                | num     |     3 | DA DECIDERE
#     DSBac_Length             | num     |     8 | DA DECIDERE
#     DSBac_ExamDate           | cat/str |   253 | DA DECIDERE
#     DSFor_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     DSFor_Q1a                | num     |     3 | DA DECIDERE
#     DSFor_Q1b                | num     |     3 | DA DECIDERE
#     DSFor_Q2a                | num     |     3 | DA DECIDERE
#     DSFor_Q2b                | num     |     3 | DA DECIDERE
#     DSFor_Q3a                | num     |     3 | DA DECIDERE
#     DSFor_Q3b                | num     |     3 | DA DECIDERE
#     DSFor_Q4a                | num     |     3 | DA DECIDERE
#     DSFor_Q4b                | num     |     3 | DA DECIDERE
#     DSFor_Q5a                | num     |     3 | DA DECIDERE
#     DSFor_Q5b                | num     |     3 | DA DECIDERE
#     DSFor_Q6a                | num     |     3 | DA DECIDERE
#     DSFor_Q6b                | num     |     3 | DA DECIDERE
#     DSFor_Length             | num     |     8 | DA DECIDERE
#     DSFor_ExamDate           | cat/str |   253 | DA DECIDERE
#     LogMemIA_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     LogMemIA_TimeEnded       | num     |   115 | DA DECIDERE
#     LogMemIA_ImmediateScore  | num     |    26 | DA DECIDERE
#     LogMemIA_ExamDate        | date    |   135 | cand. DATA
#     LogMemIIA_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     LogMemIIA_TimeBegan      | num     |   117 | DA DECIDERE
#     LogMemIIA_DelayedScore   | num     |    25 | DA DECIDERE
#     LogMemIIA_ReminderGiven  | num     |     3 | DA DECIDERE
#     LogMemIIA_ExamDate       | date    |   135 | cand. DATA
#     MMSE_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     MMSE_Q1                  | num     |     2 | DA DECIDERE
#     MMSE_Q2                  | num     |     2 | DA DECIDERE
#     MMSE_Q3                  | num     |     2 | DA DECIDERE
#     MMSE_Q4                  | num     |     2 | DA DECIDERE
#     MMSE_Q5                  | num     |     2 | DA DECIDERE
#     MMSE_Q6                  | num     |     2 | DA DECIDERE
#     MMSE_Q7                  | num     |     2 | DA DECIDERE
#     MMSE_Q8                  | num     |     2 | DA DECIDERE
#     MMSE_Q9                  | num     |     2 | DA DECIDERE
#     MMSE_Q10                 | num     |     2 | DA DECIDERE
#     MMSE_Q11                 | num     |     2 | DA DECIDERE
#     MMSE_Q12                 | num     |     2 | DA DECIDERE
#     MMSE_Q13                 | num     |     2 | DA DECIDERE
#     MMSE_Q13a                | num     |     6 | DA DECIDERE
#     MMSE_Q14                 | num     |     2 | DA DECIDERE
#     MMSE_Q15                 | num     |     2 | DA DECIDERE
#     MMSE_Q16                 | num     |     2 | DA DECIDERE
#     MMSE_Q17                 | num     |     2 | DA DECIDERE
#     MMSE_Q18                 | num     |     2 | DA DECIDERE
#     MMSE_Q14value            | cat/str |     4 | DA DECIDERE
#     MMSE_Q15value            | cat/str |     8 | DA DECIDERE
#     MMSE_Q16value            | cat/str |     7 | DA DECIDERE
#     MMSE_Q17value            | cat/str |     9 | DA DECIDERE
#     MMSE_Q18value            | cat/str |     7 | DA DECIDERE
#     MMSE_Q19                 | num     |     2 | DA DECIDERE
#     MMSE_Q20                 | num     |     2 | DA DECIDERE
#     MMSE_Q21                 | num     |     2 | DA DECIDERE
#     MMSE_Q22                 | num     |     2 | DA DECIDERE
#     MMSE_Q23                 | num     |     2 | DA DECIDERE
#     MMSE_Q24                 | num     |     2 | DA DECIDERE
#     MMSE_Q25                 | num     |     2 | DA DECIDERE
#     MMSE_Q26                 | num     |     2 | DA DECIDERE
#     MMSE_Q27                 | num     |     2 | DA DECIDERE
#     MMSE_Q28                 | num     |     2 | DA DECIDERE
#     MMSE_Q29                 | num     |     2 | DA DECIDERE
#     MMSE_Q30                 | num     |     2 | DA DECIDERE
#     MMSE_ExamDate            | cat/str |   206 | DA DECIDERE
#     TMT_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     TMT_PtA_Complete         | num     |    74 | DA DECIDERE
#     TMT_PtA_Comission        | num     |     4 | DA DECIDERE
#     TMT_PtA_Omission         | num     |    12 | DA DECIDERE
#     TMT_PtB_Complete         | num     |   123 | DA DECIDERE
#     TMT_PtB_Comission        | num     |     9 | DA DECIDERE
#     TMT_PtB_Omission         | num     |    20 | DA DECIDERE
#     TMT_ExamDate             | cat/str |   253 | DA DECIDERE
#     WAISR_QuestionnaireNotAttempted | num     |     2 | DA DECIDERE
#     WAISR_Score              | num     |    66 | DA DECIDERE
#     WAISR_ExamDate           | cat/str |   253 | DA DECIDERE
#     update_stamp             | date    |    19 | cand. DATA
# ------------------------------------------------------------------------
ITEM = DatasetConfig(
    file_code="ITEM",                          # <-- VERIFICA
    source="ITEM.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    # date_column=?  candidati (dai valori): ['LogMemIA_ExamDate', 'LogMemIIA_ExamDate', 'update_stamp']  <-- DECIDI
    viscode_reference="VISCODE",
    # 761 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['ADAS_QuestionnaireNotAttempted', 'ADAS_Q1_T1_WL1_W1_butter', 'ADAS_Q1_T1_WL1_W2_arm', 'ADAS_Q1_T1_WL1_W3_shore', 'ADAS_Q1_T1_WL1_W4_letter', 'ADAS_Q1_T1_WL1_W5_queen', 'ADAS_Q1_T1_WL1_W6_cabin', 'ADAS_Q1_T1_WL1_W7_pole', 'ADAS_Q1_T1_WL1_W8_ticket', 'ADAS_Q1_T1_WL1_W9_grass', 'ADAS_Q1_T1_WL1_W10_engine', 'ADAS_Q1_T2_WL1_W1_pole', 'ADAS_Q1_T2_WL1_W2_letter', 'ADAS_Q1_T2_WL1_W3_butter', 'ADAS_Q1_T2_WL1_W4_queen', 'ADAS_Q1_T2_WL1_W5_arm', 'ADAS_Q1_T2_WL1_W6_shore', 'ADAS_Q1_T2_WL1_W7_grass', 'ADAS_Q1_T2_WL1_W8_cabin', 'ADAS_Q1_T2_WL1_W9_ticket', 'ADAS_Q1_T2_WL1_W10_engine', 'ADAS_Q1_T3_WL1_W1_shore', 'ADAS_Q1_T3_WL1_W2_letter', 'ADAS_Q1_T3_WL1_W3_arm', 'ADAS_Q1_T3_WL1_W4_cabin', 'ADAS_Q1_T3_WL1_W5_pole', 'ADAS_Q1_T3_WL1_W6_ticket', 'ADAS_Q1_T3_WL1_W7_engine', 'ADAS_Q1_T3_WL1_W8_grass', 'ADAS_Q1_T3_WL1_W9_butter', 'ADAS_Q1_T3_WL1_W10_queen', 'ADAS_Q1_T1_WL2_W1_bottle', 'ADAS_Q1_T1_WL2_W2_potato', 'ADAS_Q1_T1_WL2_W3_girl', 'ADAS_Q1_T1_WL2_W4_temple', 'ADAS_Q1_T1_WL2_W5_star', 'ADAS_Q1_T1_WL2_W6_animal', 'ADAS_Q1_T1_WL2_W7_forest', 'ADAS_Q1_T1_WL2_W8_lake', 'ADAS_Q1_T1_WL2_W9_clock', 'ADAS_Q1_T1_WL2_W10_office', 'ADAS_Q1_T2_WL2_W1_forest', 'ADAS_Q1_T2_WL2_W2_temple', 'ADAS_Q1_T2_WL2_W3_bottle', 'ADAS_Q1_T2_WL2_W4_star', 'ADAS_Q1_T2_WL2_W5_potato', 'ADAS_Q1_T2_WL2_W6_girl', 'ADAS_Q1_T2_WL2_W7_clock', 'ADAS_Q1_T2_WL2_W8_animal', 'ADAS_Q1_T2_WL2_W9_lake', 'ADAS_Q1_T2_WL2_W10_office', 'ADAS_Q1_T3_WL2_W1_girl', 'ADAS_Q1_T3_WL2_W2_temple', 'ADAS_Q1_T3_WL2_W3_potato', 'ADAS_Q1_T3_WL2_W4_animal', 'ADAS_Q1_T3_WL2_W5_forest', 'ADAS_Q1_T3_WL2_W6_lake', 'ADAS_Q1_T3_WL2_W7_office', 'ADAS_Q1_T3_WL2_W8_clock', 'ADAS_Q1_T3_WL2_W9_bottle', 'ADAS_Q1_T3_WL2_W10_star', 'ADAS_Q1_T1_WL3_W1_coast', 'ADAS_Q1_T1_WL3_W2_doll', 'ADAS_Q1_T1_WL3_W3_lip', 'ADAS_Q1_T1_WL3_W4_chair', 'ADAS_Q1_T1_WL3_W5_student', 'ADAS_Q1_T1_WL3_W6_apple', 'ADAS_Q1_T1_WL3_W7_horse', 'ADAS_Q1_T1_WL3_W8_pipe', 'ADAS_Q1_T1_WL3_W9_valley', 'ADAS_Q1_T1_WL3_W10_rock', 'ADAS_Q1_T2_WL3_W1_horse', 'ADAS_Q1_T2_WL3_W2_chair', 'ADAS_Q1_T2_WL3_W3_coast', 'ADAS_Q1_T2_WL3_W4_student', 'ADAS_Q1_T2_WL3_W5_doll', 'ADAS_Q1_T2_WL3_W6_lip', 'ADAS_Q1_T2_WL3_W7_valley', 'ADAS_Q1_T2_WL3_W8_apple', 'ADAS_Q1_T2_WL3_W9_pipe', 'ADAS_Q1_T2_WL3_W10_rock', 'ADAS_Q1_T3_WL3_W1_lip', 'ADAS_Q1_T3_WL3_W2_chair', 'ADAS_Q1_T3_WL3_W3_doll', 'ADAS_Q1_T3_WL3_W4_apple', 'ADAS_Q1_T3_WL3_W5_horse', 'ADAS_Q1_T3_WL3_W6_pipe', 'ADAS_Q1_T3_WL3_W7_rock', 'ADAS_Q1_T3_WL3_W8_valley', 'ADAS_Q1_T3_WL3_W9_coast', 'ADAS_Q1_T3_WL3_W10_student', 'ADAS_Q1_TimeEnded', 'ADAS_Q2a', 'ADAS_Q2b', 'ADAS_Q2c', 'ADAS_Q2d', 'ADAS_Q2e', 'ADAS_Q3a', 'ADAS_Q3b', 'ADAS_Q3c', 'ADAS_Q3d', 'ADAS_Q4_TimeBegan', 'ADAS_Q4_WL1_W1_butter', 'ADAS_Q4_WL1_W2_arm', 'ADAS_Q4_WL1_W3_shore', 'ADAS_Q4_WL1_W4_letter', 'ADAS_Q4_WL1_W5_queen', 'ADAS_Q4_WL1_W6_cabin', 'ADAS_Q4_WL1_W7_pole', 'ADAS_Q4_WL1_W8_ticket', 'ADAS_Q4_WL1_W9_grass', 'ADAS_Q4_WL1_W10_engine', 'ADAS_Q4_WL2_W1_bottle', 'ADAS_Q4_WL2_W2_potato', 'ADAS_Q4_WL2_W3_girl', 'ADAS_Q4_WL2_W4_temple', 'ADAS_Q4_WL2_W5_star', 'ADAS_Q4_WL2_W6_animal', 'ADAS_Q4_WL2_W7_forest', 'ADAS_Q4_WL2_W8_lake', 'ADAS_Q4_WL2_W9_clock', 'ADAS_Q4_WL2_W10_office', 'ADAS_Q4_WL3_W1_coast', 'ADAS_Q4_WL3_W2_doll', 'ADAS_Q4_WL3_W3_lip', 'ADAS_Q4_WL3_W4_chair', 'ADAS_Q4_WL3_W5_student', 'ADAS_Q4_WL3_W6_apple', 'ADAS_Q4_WL3_W7_horse', 'ADAS_Q4_WL3_W8_pipe', 'ADAS_Q4_WL3_W9_valley', 'ADAS_Q4_WL3_W10_rock', 'ADAS_Q5a_Flower', 'ADAS_Q5a_Bed', 'ADAS_Q5a_Whistle', 'ADAS_Q5a_Pencil', 'ADAS_Q5a_Rattle', 'ADAS_Q5a_Mask', 'ADAS_Q5a_Scissors', 'ADAS_Q5a_Comb', 'ADAS_Q5a_Wallet', 'ADAS_Q5a_Harmonica', 'ADAS_Q5a_Stethoscope', 'ADAS_Q5a_Tongs', 'ADAS_Q5b_Thumb', 'ADAS_Q5b_Middle', 'ADAS_Q5b_Ring', 'ADAS_Q5b_Index', 'ADAS_Q5b_Pinky', 'ADAS_Q6a', 'ADAS_Q6b', 'ADAS_Q6c', 'ADAS_Q6d', 'ADAS_Q6e', 'ADAS_Q7a', 'ADAS_Q7b', 'ADAS_Q7c', 'ADAS_Q7d', 'ADAS_Q7e', 'ADAS_Q7f', 'ADAS_Q7g', 'ADAS_Q7h', 'ADAS_Q8_WL1_REC_W1_nurse', 'ADAS_Q8_WL1_REC_W2_magazine', 'ADAS_Q8_WL1_REC_W3_wizard', 'ADAS_Q8_WL1_REC_W4_van', 'ADAS_Q8_WL1_REC_W5_leopard', 'ADAS_Q8_WL1_REC_W6_sale', 'ADAS_Q8_WL1_REC_W7_sea', 'ADAS_Q8_WL1_REC_W8_train', 'ADAS_Q8_WL1_REC_W9_coin', 'ADAS_Q8_WL1_REC_W10_ship', 'ADAS_Q8_WL1_REC_W11_institution', 'ADAS_Q8_WL1_REC_W12_map', 'ADAS_Q8_WL1_REC_W13_axe', 'ADAS_Q8_WL1_REC_W14_board', 'ADAS_Q8_WL1_REC_W15_carrot', 'ADAS_Q8_WL1_REC_W16_milk', 'ADAS_Q8_WL1_REC_W17_volume', 'ADAS_Q8_WL1_REC_W18_forest', 'ADAS_Q8_WL1_REC_W19_anchor', 'ADAS_Q8_WL1_REC_W20_gem', 'ADAS_Q8_WL1_REC_W21_cat', 'ADAS_Q8_WL1_REC_W22_fund', 'ADAS_Q8_WL1_REC_W23_edge', 'ADAS_Q8_WL1_REC_W24_cake', 'ADAS_Q8_WL1_Reminder_W1_nurse', 'ADAS_Q8_WL1_Reminder_W2_magazine', 'ADAS_Q8_WL1_Reminder_W3_wizard', 'ADAS_Q8_WL1_Reminder_W4_van', 'ADAS_Q8_WL1_Reminder_W5_leopard', 'ADAS_Q8_WL1_Reminder_W6_sale', 'ADAS_Q8_WL1_Reminder_W7_sea', 'ADAS_Q8_WL1_Reminder_W8_train', 'ADAS_Q8_WL1_Reminder_W9_coin', 'ADAS_Q8_WL1_Reminder_W10_ship', 'ADAS_Q8_WL1_Reminder_W11_institution', 'ADAS_Q8_WL1_Reminder_W12_map', 'ADAS_Q8_WL1_Reminder_W13_axe', 'ADAS_Q8_WL1_Reminder_W14_board', 'ADAS_Q8_WL1_Reminder_W15_carrot', 'ADAS_Q8_WL1_Reminder_W16_milk', 'ADAS_Q8_WL1_Reminder_W17_volume', 'ADAS_Q8_WL1_Reminder_W18_forest', 'ADAS_Q8_WL1_Reminder_W19_anchor', 'ADAS_Q8_WL1_Reminder_W20_gem', 'ADAS_Q8_WL1_Reminder_W21_cat', 'ADAS_Q8_WL1_Reminder_W22_fund', 'ADAS_Q8_WL1_Reminder_W23_edge', 'ADAS_Q8_WL1_Reminder_W24_cake', 'ADAS_Q8_WL2_REC_W1_cost', 'ADAS_Q8_WL2_REC_W2_nation', 'ADAS_Q8_WL2_REC_W3_chimney', 'ADAS_Q8_WL2_REC_W4_sparrow', 'ADAS_Q8_WL2_REC_W5_damages', 'ADAS_Q8_WL2_REC_W6_traffic', 'ADAS_Q8_WL2_REC_W7_sandwich', 'ADAS_Q8_WL2_REC_W8_service', 'ADAS_Q8_WL2_REC_W9_shell', 'ADAS_Q8_WL2_REC_W10_solution', 'ADAS_Q8_WL2_REC_W11_yard', 'ADAS_Q8_WL2_REC_W12_tube', 'ADAS_Q8_WL2_REC_W13_body', 'ADAS_Q8_WL2_REC_W14_ground', 'ADAS_Q8_WL2_REC_W15_stick', 'ADAS_Q8_WL2_REC_W16_engine', 'ADAS_Q8_WL2_REC_W17_riches', 'ADAS_Q8_WL2_REC_W18_gravity', 'ADAS_Q8_WL2_REC_W19_summer', 'ADAS_Q8_WL2_REC_W20_wisdom', 'ADAS_Q8_WL2_REC_W21_man', 'ADAS_Q8_WL2_REC_W22_meal', 'ADAS_Q8_WL2_REC_W23_passenger', 'ADAS_Q8_WL2_REC_W24_acid', 'ADAS_Q8_WL2_Reminder_W1_cost', 'ADAS_Q8_WL2_Reminder_W2_nation', 'ADAS_Q8_WL2_Reminder_W3_chimney', 'ADAS_Q8_WL2_Reminder_W4_sparrow', 'ADAS_Q8_WL2_Reminder_W5_damages', 'ADAS_Q8_WL2_Reminder_W6_traffic', 'ADAS_Q8_WL2_Reminder_W7_sandwich', 'ADAS_Q8_WL2_Reminder_W8_service', 'ADAS_Q8_WL2_Reminder_W9_shell', 'ADAS_Q8_WL2_Reminder_W10_solution', 'ADAS_Q8_WL2_Reminder_W11_yard', 'ADAS_Q8_WL2_Reminder_W12_tube', 'ADAS_Q8_WL2_Reminder_W13_body', 'ADAS_Q8_WL2_Reminder_W14_ground', 'ADAS_Q8_WL2_Reminder_W15_stick', 'ADAS_Q8_WL2_Reminder_W16_engine', 'ADAS_Q8_WL2_Reminder_W17_riches', 'ADAS_Q8_WL2_Reminder_W18_gravity', 'ADAS_Q8_WL2_Reminder_W19_summer', 'ADAS_Q8_WL2_Reminder_W20_wisdom', 'ADAS_Q8_WL2_Reminder_W21_man', 'ADAS_Q8_WL2_Reminder_W22_meal', 'ADAS_Q8_WL2_Reminder_W23_passenger', 'ADAS_Q8_WL2_Reminder_W24_acid', 'ADAS_Q8_WL3_REC_W1_silence', 'ADAS_Q8_WL3_REC_W2_elbow', 'ADAS_Q8_WL3_REC_W3_daughter', 'ADAS_Q8_WL3_REC_W4_powder', 'ADAS_Q8_WL3_REC_W5_canal', 'ADAS_Q8_WL3_REC_W6_forehead', 'ADAS_Q8_WL3_REC_W7_tiger', 'ADAS_Q8_WL3_REC_W8_twilight', 'ADAS_Q8_WL3_REC_W9_dragon', 'ADAS_Q8_WL3_REC_W10_chamber', 'ADAS_Q8_WL3_REC_W11_sister', 'ADAS_Q8_WL3_REC_W12_beggar', 'ADAS_Q8_WL3_REC_W13_echo', 'ADAS_Q8_WL3_REC_W14_nephew', 'ADAS_Q8_WL3_REC_W15_duty', 'ADAS_Q8_WL3_REC_W16_village', 'ADAS_Q8_WL3_REC_W17_corner', 'ADAS_Q8_WL3_REC_W18_olive', 'ADAS_Q8_WL3_REC_W19_music', 'ADAS_Q8_WL3_REC_W20_courage', 'ADAS_Q8_WL3_REC_W21_bushel', 'ADAS_Q8_WL3_REC_W22_ribbon', 'ADAS_Q8_WL3_REC_W23_object', 'ADAS_Q8_WL3_REC_W24_collar', 'ADAS_Q8_WL3_Reminder_W1_silence', 'ADAS_Q8_WL3_Reminder_W2_elbow', 'ADAS_Q8_WL3_Reminder_W3_daughter', 'ADAS_Q8_WL3_Reminder_W4_powder', 'ADAS_Q8_WL3_Reminder_W5_canal', 'ADAS_Q8_WL3_Reminder_W6_forehead', 'ADAS_Q8_WL3_Reminder_W7_tiger', 'ADAS_Q8_WL3_Reminder_W8_twilight', 'ADAS_Q8_WL3_Reminder_W9_dragon', 'ADAS_Q8_WL3_Reminder_W10_chamber', 'ADAS_Q8_WL3_Reminder_W11_sister', 'ADAS_Q8_WL3_Reminder_W12_beggar', 'ADAS_Q8_WL3_Reminder_W13_echo', 'ADAS_Q8_WL3_Reminder_W14_nephew', 'ADAS_Q8_WL3_Reminder_W15_duty', 'ADAS_Q8_WL3_Reminder_W16_village', 'ADAS_Q8_WL3_Reminder_W17_corner', 'ADAS_Q8_WL3_Reminder_W18_olive', 'ADAS_Q8_WL3_Reminder_W19_music', 'ADAS_Q8_WL3_Reminder_W20_courage', 'ADAS_Q8_WL3_Reminder_W21_bushel', 'ADAS_Q8_WL3_Reminder_W22_ribbon', 'ADAS_Q8_WL3_Reminder_W23_object', 'ADAS_Q8_WL3_Reminder_W24_collar', 'ADAS_Q9', 'ADAS_Q10', 'ADAS_Q11', 'ADAS_Q12', 'ADAS_Q13a', 'ADAS_Q13b', 'ADAS_Q13c', 'ADAS_ExamDate', 'ANART_QuestionnaireNotAttempted', 'ANART_Q1', 'ANART_Q2', 'ANART_Q3', 'ANART_Q4', 'ANART_Q5', 'ANART_Q6', 'ANART_Q7', 'ANART_Q8', 'ANART_Q9', 'ANART_Q10', 'ANART_Q11', 'ANART_Q12', 'ANART_Q13', 'ANART_Q14', 'ANART_Q15', 'ANART_Q16', 'ANART_Q17', 'ANART_Q18', 'ANART_Q19', 'ANART_Q20', 'ANART_Q21', 'ANART_Q22', 'ANART_Q23', 'ANART_Q24', 'ANART_Q25', 'ANART_Q26', 'ANART_Q27', 'ANART_Q28', 'ANART_Q29', 'ANART_Q30', 'ANART_Q31', 'ANART_Q32', 'ANART_Q33', 'ANART_Q34', 'ANART_Q35', 'ANART_Q36', 'ANART_Q37', 'ANART_Q38', 'ANART_Q39', 'ANART_Q40', 'ANART_Q41', 'ANART_Q42', 'ANART_Q43', 'ANART_Q44', 'ANART_Q45', 'ANART_Q46', 'ANART_Q47', 'ANART_Q48', 'ANART_Q49', 'ANART_Q50', 'ANART_ExamDate', 'AVLT_QuestionnaireNotAttempted', 'AVLT_StartTime', 'AVLTA_WL1a_T1_W1_drum', 'AVLTA_WL1a_T1_W2_curtain', 'AVLTA_WL1a_T1_W3_bell', 'AVLTA_WL1a_T1_W4_coffee', 'AVLTA_WL1a_T1_W5_school', 'AVLTA_WL1a_T1_W6_parent', 'AVLTA_WL1a_T1_W7_moon', 'AVLTA_WL1a_T1_W8_garden', 'AVLTA_WL1a_T1_W9_hat', 'AVLTA_WL1a_T1_W10_farmer', 'AVLTA_WL1a_T1_W11_nose', 'AVLTA_WL1a_T1_W12_turkey', 'AVLTA_WL1a_T1_W13_color', 'AVLTA_WL1a_T1_W14_house', 'AVLTA_WL1a_T1_W15_river', 'AVLTA_WL1a_T2_W1_drum', 'AVLTA_WL1a_T2_W2_curtain', 'AVLTA_WL1a_T2_W3_bell', 'AVLTA_WL1a_T2_W4_coffee', 'AVLTA_WL1a_T2_W5_school', 'AVLTA_WL1a_T2_W6_parent', 'AVLTA_WL1a_T2_W7_moon', 'AVLTA_WL1a_T2_W8_garden', 'AVLTA_WL1a_T2_W9_hat', 'AVLTA_WL1a_T2_W10_farmer', 'AVLTA_WL1a_T2_W11_nose', 'AVLTA_WL1a_T2_W12_turkey', 'AVLTA_WL1a_T2_W13_color', 'AVLTA_WL1a_T2_W14_house', 'AVLTA_WL1a_T2_W15_river', 'AVLTA_WL1a_T3_W1_drum', 'AVLTA_WL1a_T3_W2_curtain', 'AVLTA_WL1a_T3_W3_bell', 'AVLTA_WL1a_T3_W4_coffee', 'AVLTA_WL1a_T3_W5_school', 'AVLTA_WL1a_T3_W6_parent', 'AVLTA_WL1a_T3_W7_moon', 'AVLTA_WL1a_T3_W8_garden', 'AVLTA_WL1a_T3_W9_hat', 'AVLTA_WL1a_T3_W10_farmer', 'AVLTA_WL1a_T3_W11_nose', 'AVLTA_WL1a_T3_W12_turkey', 'AVLTA_WL1a_T3_W13_color', 'AVLTA_WL1a_T3_W14_house', 'AVLTA_WL1a_T3_W15_river', 'AVLTA_WL1a_T4_W1_drum', 'AVLTA_WL1a_T4_W2_curtain', 'AVLTA_WL1a_T4_W3_bell', 'AVLTA_WL1a_T4_W4_coffee', 'AVLTA_WL1a_T4_W5_school', 'AVLTA_WL1a_T4_W6_parent', 'AVLTA_WL1a_T4_W7_moon', 'AVLTA_WL1a_T4_W8_garden', 'AVLTA_WL1a_T4_W9_hat', 'AVLTA_WL1a_T4_W10_farmer', 'AVLTA_WL1a_T4_W11_nose', 'AVLTA_WL1a_T4_W12_turkey', 'AVLTA_WL1a_T4_W13_color', 'AVLTA_WL1a_T4_W14_house', 'AVLTA_WL1a_T4_W15_river', 'AVLTA_WL1a_T5_W1_drum', 'AVLTA_WL1a_T5_W2_curtain', 'AVLTA_WL1a_T5_W3_bell', 'AVLTA_WL1a_T5_W4_coffee', 'AVLTA_WL1a_T5_W5_school', 'AVLTA_WL1a_T5_W6_parent', 'AVLTA_WL1a_T5_W7_moon', 'AVLTA_WL1a_T5_W8_garden', 'AVLTA_WL1a_T5_W9_hat', 'AVLTA_WL1a_T5_W10_farmer', 'AVLTA_WL1a_T5_W11_nose', 'AVLTA_WL1a_T5_W12_turkey', 'AVLTA_WL1a_T5_W13_color', 'AVLTA_WL1a_T5_W14_house', 'AVLTA_WL1a_T5_W15_river', 'AVLTA_WL1a_T6_W1_drum', 'AVLTA_WL1a_T6_W2_curtain', 'AVLTA_WL1a_T6_W3_bell', 'AVLTA_WL1a_T6_W4_coffee', 'AVLTA_WL1a_T6_W5_school', 'AVLTA_WL1a_T6_W6_parent', 'AVLTA_WL1a_T6_W7_moon', 'AVLTA_WL1a_T6_W8_garden', 'AVLTA_WL1a_T6_W9_hat', 'AVLTA_WL1a_T6_W10_farmer', 'AVLTA_WL1a_T6_W11_nose', 'AVLTA_WL1a_T6_W12_turkey', 'AVLTA_WL1a_T6_W13_color', 'AVLTA_WL1a_T6_W14_house', 'AVLTA_WL1a_T6_W15_river', 'AVLTA_WL1b_T7_W1_desk', 'AVLTA_WL1b_T7_W2_ranger', 'AVLTA_WL1b_T7_W3_bird', 'AVLTA_WL1b_T7_W4_shoe', 'AVLTA_WL1b_T7_W5_stove', 'AVLTA_WL1b_T7_W6_mountain', 'AVLTA_WL1b_T7_W7_glasses', 'AVLTA_WL1b_T7_W8_towel', 'AVLTA_WL1b_T7_W9_cloud', 'AVLTA_WL1b_T7_W10_boat', 'AVLTA_WL1b_T7_W11_lamb', 'AVLTA_WL1b_T7_W12_gun', 'AVLTA_WL1b_T7_W13_pencil', 'AVLTA_WL1b_T7_W14_church', 'AVLTA_WL1b_T7_W15_fish', 'AVLTB_WL2a_T1_W1_doll', 'AVLTB_WL2a_T1_W2_mirror', 'AVLTB_WL2a_T1_W3_nail', 'AVLTB_WL2a_T1_W4_sailor', 'AVLTB_WL2a_T1_W5_heart', 'AVLTB_WL2a_T1_W6_desert', 'AVLTB_WL2a_T1_W7_face', 'AVLTB_WL2a_T1_W8_letter', 'AVLTB_WL2a_T1_W9_bed', 'AVLTB_WL2a_T1_W10_machine', 'AVLTB_WL2a_T1_W11_milk', 'AVLTB_WL2a_T1_W12_helmet', 'AVLTB_WL2a_T1_W13_music', 'AVLTB_WL2a_T1_W14_horse', 'AVLTB_WL2a_T1_W15_road', 'AVLTB_WL2a_T2_W1_doll', 'AVLTB_WL2a_T2_W2_mirror', 'AVLTB_WL2a_T2_W3_nail', 'AVLTB_WL2a_T2_W4_sailor', 'AVLTB_WL2a_T2_W5_heart', 'AVLTB_WL2a_T2_W6_desert', 'AVLTB_WL2a_T2_W7_face', 'AVLTB_WL2a_T2_W8_letter', 'AVLTB_WL2a_T2_W9_bed', 'AVLTB_WL2a_T2_W10_machine', 'AVLTB_WL2a_T2_W11_milk', 'AVLTB_WL2a_T2_W12_helmet', 'AVLTB_WL2a_T2_W13_music', 'AVLTB_WL2a_T2_W14_horse', 'AVLTB_WL2a_T2_W15_road', 'AVLTB_WL2a_T3_W1_doll', 'AVLTB_WL2a_T3_W2_mirror', 'AVLTB_WL2a_T3_W3_nail', 'AVLTB_WL2a_T3_W4_sailor', 'AVLTB_WL2a_T3_W5_heart', 'AVLTB_WL2a_T3_W6_desert', 'AVLTB_WL2a_T3_W7_face', 'AVLTB_WL2a_T3_W8_letter', 'AVLTB_WL2a_T3_W9_bed', 'AVLTB_WL2a_T3_W10_machine', 'AVLTB_WL2a_T3_W11_milk', 'AVLTB_WL2a_T3_W12_helmet', 'AVLTB_WL2a_T3_W13_music', 'AVLTB_WL2a_T3_W14_horse', 'AVLTB_WL2a_T3_W15_road', 'AVLTB_WL2a_T4_W1_doll', 'AVLTB_WL2a_T4_W2_mirror', 'AVLTB_WL2a_T4_W3_nail', 'AVLTB_WL2a_T4_W4_sailor', 'AVLTB_WL2a_T4_W5_heart', 'AVLTB_WL2a_T4_W6_desert', 'AVLTB_WL2a_T4_W7_face', 'AVLTB_WL2a_T4_W8_letter', 'AVLTB_WL2a_T4_W9_bed', 'AVLTB_WL2a_T4_W10_machine', 'AVLTB_WL2a_T4_W11_milk', 'AVLTB_WL2a_T4_W12_helmet', 'AVLTB_WL2a_T4_W13_music', 'AVLTB_WL2a_T4_W14_horse', 'AVLTB_WL2a_T4_W15_road', 'AVLTB_WL2a_T5_W1_doll', 'AVLTB_WL2a_T5_W2_mirror', 'AVLTB_WL2a_T5_W3_nail', 'AVLTB_WL2a_T5_W4_sailor', 'AVLTB_WL2a_T5_W5_heart', 'AVLTB_WL2a_T5_W6_desert', 'AVLTB_WL2a_T5_W7_face', 'AVLTB_WL2a_T5_W8_letter', 'AVLTB_WL2a_T5_W9_bed', 'AVLTB_WL2a_T5_W10_machine', 'AVLTB_WL2a_T5_W11_milk', 'AVLTB_WL2a_T5_W12_helmet', 'AVLTB_WL2a_T5_W13_music', 'AVLTB_WL2a_T5_W14_horse', 'AVLTB_WL2a_T5_W15_road', 'AVLTB_WL2a_T6_W1_doll', 'AVLTB_WL2a_T6_W2_mirror', 'AVLTB_WL2a_T6_W3_nail', 'AVLTB_WL2a_T6_W4_sailor', 'AVLTB_WL2a_T6_W5_heart', 'AVLTB_WL2a_T6_W6_desert', 'AVLTB_WL2a_T6_W7_face', 'AVLTB_WL2a_T6_W8_letter', 'AVLTB_WL2a_T6_W9_bed', 'AVLTB_WL2a_T6_W10_machine', 'AVLTB_WL2a_T6_W11_milk', 'AVLTB_WL2a_T6_W12_helmet', 'AVLTB_WL2a_T6_W13_music', 'AVLTB_WL2a_T6_W14_horse', 'AVLTB_WL2a_T6_W15_road', 'AVLTB_WL2b_T7_W1_dish', 'AVLTB_WL2b_T7_W2_jester', 'AVLTB_WL2b_T7_W3_hill', 'AVLTB_WL2b_T7_W4_coat', 'AVLTB_WL2b_T7_W5_tool', 'AVLTB_WL2b_T7_W6_forest', 'AVLTB_WL2b_T7_W7_water', 'AVLTB_WL2b_T7_W8_ladder', 'AVLTB_WL2b_T7_W9_girl', 'AVLTB_WL2b_T7_W10_foot', 'AVLTB_WL2b_T7_W11_shield', 'AVLTB_WL2b_T7_W12_pie', 'AVLTB_WL2b_T7_W13_insect', 'AVLTB_WL2b_T7_W14_ball', 'AVLTB_WL2b_T7_W15_car', 'AVLT_Trial1Int', 'AVLT_Trial2Int', 'AVLT_Trial3Int', 'AVLT_Trial4Int', 'AVLT_Trial5Int', 'AVLT_Trial6Int', 'AVLT_Trial7Int', 'AVLT_ExamDate', 'AVLT_Delay_QuestionnaireNotAttempted', 'AVLT_DelayTime', 'AVLT_Delay_WL1_W1_drum', 'AVLT_Delay_WL1_W2_curtain', 'AVLT_Delay_WL1_W3_bell', 'AVLT_Delay_WL1_W4_coffee', 'AVLT_Delay_WL1_W5_school', 'AVLT_Delay_WL1_W6_parent', 'AVLT_Delay_WL1_W7_moon', 'AVLT_Delay_WL1_W8_garden', 'AVLT_Delay_WL1_W9_hat', 'AVLT_Delay_WL1_W10_farmer', 'AVLT_Delay_WL1_W11_nose', 'AVLT_Delay_WL1_W12_turkey', 'AVLT_Delay_WL1_W13_color', 'AVLT_Delay_WL1_W14_house', 'AVLT_Delay_WL1_W15_river', 'AVLT_Delay_WL2_W1_doll', 'AVLT_Delay_WL2_W2_mirror', 'AVLT_Delay_WL2_W3_nail', 'AVLT_Delay_WL2_W4_sailor', 'AVLT_Delay_WL2_W5_heart', 'AVLT_Delay_WL2_W6_desert', 'AVLT_Delay_WL2_W7_face', 'AVLT_Delay_WL2_W8_letter', 'AVLT_Delay_WL2_W9_bed', 'AVLT_Delay_WL2_W10_machine', 'AVLT_Delay_WL2_W11_milk', 'AVLT_Delay_WL2_W12_helmet', 'AVLT_Delay_WL2_W13_music', 'AVLT_Delay_WL2_W14_horse', 'AVLT_Delay_WL2_W15_road', 'AVLT_Delay_Int', 'AVLT_Delay_Rec', 'AVLT_Delay_TotInt', 'AVLT_Delay_ExamDate', 'BosNam_QuestionnaireNotAttempted', 'BosNam_Q1', 'BosNam_Q3', 'BosNam_Q5', 'BosNam_Q7', 'BosNam_Q9', 'BosNam_Q11', 'BosNam_Q13', 'BosNam_Q15', 'BosNam_Q17', 'BosNam_Q19', 'BosNam_Q21', 'BosNam_Q23', 'BosNam_Q25', 'BosNam_Q27', 'BosNam_Q29', 'BosNam_Q31', 'BosNam_Q33', 'BosNam_Q35', 'BosNam_Q37', 'BosNam_Q39', 'BosNam_Q41', 'BosNam_Q43', 'BosNam_Q45', 'BosNam_Q47', 'BosNam_Q49', 'BosNam_Q51', 'BosNam_Q53', 'BosNam_Q55', 'BosNam_Q57', 'BosNam_Q59', 'BosNam_ExamDate', 'CatFlu_QuestionnaireNotAttempted', 'CatFlu_Practise', 'CatFlu_Animal_Total', 'CatFlu_Animal_Perseverations', 'CatFlu_Animal_Intrusions', 'CatFlu_Vegetable_Total', 'CatFlu_Vegetable_Perseverations', 'CatFlu_Vegetable_Intrusions', 'CatFlu_ExamDate', 'CDT_QuestionnaireNotAttempted', 'CDT_Q1pt1', 'CDT_Q1pt2', 'CDT_Q1pt3', 'CDT_Q1pt4', 'CDT_Q1pt5', 'CDT_Q2pt1', 'CDT_Q2pt2', 'CDT_Q2pt3', 'CDT_Q2pt4', 'CDT_Q2pt5', 'CDT_ExamDate', 'DSBac_QuestionnaireNotAttempted', 'DSBac_Q1a', 'DSBac_Q1b', 'DSBac_Q2a', 'DSBac_Q2b', 'DSBac_Q3a', 'DSBac_Q3b', 'DSBac_Q4a', 'DSBac_Q4b', 'DSBac_Q5a', 'DSBac_Q5b', 'DSBac_Q6a', 'DSBac_Q6b', 'DSBac_Length', 'DSBac_ExamDate', 'DSFor_QuestionnaireNotAttempted', 'DSFor_Q1a', 'DSFor_Q1b', 'DSFor_Q2a', 'DSFor_Q2b', 'DSFor_Q3a', 'DSFor_Q3b', 'DSFor_Q4a', 'DSFor_Q4b', 'DSFor_Q5a', 'DSFor_Q5b', 'DSFor_Q6a', 'DSFor_Q6b', 'DSFor_Length', 'DSFor_ExamDate', 'LogMemIA_QuestionnaireNotAttempted', 'LogMemIA_TimeEnded', 'LogMemIA_ImmediateScore', 'LogMemIIA_QuestionnaireNotAttempted', 'LogMemIIA_TimeBegan', 'LogMemIIA_DelayedScore', 'LogMemIIA_ReminderGiven', 'MMSE_QuestionnaireNotAttempted', 'MMSE_Q1', 'MMSE_Q2', 'MMSE_Q3', 'MMSE_Q4', 'MMSE_Q5', 'MMSE_Q6', 'MMSE_Q7', 'MMSE_Q8', 'MMSE_Q9', 'MMSE_Q10', 'MMSE_Q11', 'MMSE_Q12', 'MMSE_Q13', 'MMSE_Q13a', 'MMSE_Q14', 'MMSE_Q15', 'MMSE_Q16', 'MMSE_Q17', 'MMSE_Q18', 'MMSE_Q14value', 'MMSE_Q15value', 'MMSE_Q16value', 'MMSE_Q17value', 'MMSE_Q18value', 'MMSE_Q19', 'MMSE_Q20', 'MMSE_Q21', 'MMSE_Q22', 'MMSE_Q23', 'MMSE_Q24', 'MMSE_Q25', 'MMSE_Q26', 'MMSE_Q27', 'MMSE_Q28', 'MMSE_Q29', 'MMSE_Q30', 'MMSE_ExamDate', 'TMT_QuestionnaireNotAttempted', 'TMT_PtA_Complete', 'TMT_PtA_Comission', 'TMT_PtA_Omission', 'TMT_PtB_Complete', 'TMT_PtB_Comission', 'TMT_PtB_Omission', 'TMT_ExamDate', 'WAISR_QuestionnaireNotAttempted', 'WAISR_Score', 'WAISR_ExamDate']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# MMSE
#   source: MMSE_25Jul2025.csv   |   righe campionate: 500   |   colonne: 58
#   INDIZIO categoria dal nome (NON deciso): ['scale']
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   482 | cand. ID
#     RID                      | num     |   482 | cand. ID
#     VISCODE                  | cat/str |     3 | cand. VISITA
#     VISCODE2                 | cat/str |     3 | cand. VISITA
#     VISDATE                  | date    |   155 | cand. DATA
#     DONE                     | vuota   |     0 | DA DECIDERE
#     NDREASON                 | vuota   |     0 | DA DECIDERE
#     SOURCE                   | vuota   |     0 | DA DECIDERE
#     MMDATE                   | num     |     2 | DA DECIDERE
#     MMYEAR                   | num     |     2 | DA DECIDERE
#     MMMONTH                  | num     |     2 | DA DECIDERE
#     MMDAY                    | num     |     2 | DA DECIDERE
#     MMSEASON                 | num     |     2 | DA DECIDERE
#     MMHOSPIT                 | num     |     2 | DA DECIDERE
#     MMFLOOR                  | num     |     2 | DA DECIDERE
#     MMCITY                   | num     |     2 | DA DECIDERE
#     MMAREA                   | num     |     2 | DA DECIDERE
#     MMSTATE                  | num     |     2 | DA DECIDERE
#     WORDLIST                 | vuota   |     0 | DA DECIDERE
#     WORD1                    | num     |     2 | DA DECIDERE
#     WORD2                    | num     |     2 | DA DECIDERE
#     WORD3                    | num     |     2 | DA DECIDERE
#     MMTRIALS                 | num     |     4 | DA DECIDERE
#     MMD                      | num     |     2 | DA DECIDERE
#     MML                      | num     |     2 | DA DECIDERE
#     MMR                      | num     |     2 | DA DECIDERE
#     MMO                      | num     |     2 | DA DECIDERE
#     MMW                      | num     |     2 | DA DECIDERE
#     MMLTR1                   | vuota   |     0 | DA DECIDERE
#     MMLTR2                   | vuota   |     0 | DA DECIDERE
#     MMLTR3                   | vuota   |     0 | DA DECIDERE
#     MMLTR4                   | vuota   |     0 | DA DECIDERE
#     MMLTR5                   | vuota   |     0 | DA DECIDERE
#     MMLTR6                   | vuota   |     0 | DA DECIDERE
#     MMLTR7                   | vuota   |     0 | DA DECIDERE
#     WORLDSCORE               | vuota   |     0 | DA DECIDERE
#     WORD1DL                  | num     |     2 | DA DECIDERE
#     WORD2DL                  | num     |     2 | DA DECIDERE
#     WORD3DL                  | num     |     2 | DA DECIDERE
#     MMWATCH                  | num     |     2 | DA DECIDERE
#     MMPENCIL                 | num     |     2 | DA DECIDERE
#     MMREPEAT                 | num     |     2 | DA DECIDERE
#     MMHAND                   | num     |     2 | DA DECIDERE
#     MMFOLD                   | num     |     2 | DA DECIDERE
#     MMONFLR                  | num     |     2 | DA DECIDERE
#     MMREAD                   | num     |     1 | DA DECIDERE
#     MMWRITE                  | num     |     2 | DA DECIDERE
#     MMDRAW                   | num     |     2 | DA DECIDERE
#     MMSCORE                  | num     |    17 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   157 | cand. DATA
#     USERDATE2                | vuota   |     0 | DA DECIDERE
#     update_stamp             | date    |    64 | cand. DATA
# ------------------------------------------------------------------------
MMSE = DatasetConfig(
    file_code="MMSE",                          # <-- VERIFICA
    source="MMSE_25Jul2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['scale'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['VISDATE', 'update_stamp']) VERIFICA
    # 45 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['DONE', 'NDREASON', 'SOURCE', 'MMDATE', 'MMYEAR', 'MMMONTH', 'MMDAY', 'MMSEASON', 'MMHOSPIT', 'MMFLOOR', 'MMCITY', 'MMAREA', 'MMSTATE', 'WORDLIST', 'WORD1', 'WORD2', 'WORD3', 'MMTRIALS', 'MMD', 'MML', 'MMR', 'MMO', 'MMW', 'MMLTR1', 'MMLTR2', 'MMLTR3', 'MMLTR4', 'MMLTR5', 'MMLTR6', 'MMLTR7', 'WORLDSCORE', 'WORD1DL', 'WORD2DL', 'WORD3DL', 'MMWATCH', 'MMPENCIL', 'MMREPEAT', 'MMHAND', 'MMFOLD', 'MMONFLR', 'MMREAD', 'MMWRITE', 'MMDRAW', 'MMSCORE', 'USERDATE2']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# MOCA
#   source: MOCA_28Oct2025.csv   |   righe campionate: 500   |   colonne: 58
#   INDIZIO categoria dal nome (NON deciso): ['scale']
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   360 | cand. ID
#     RID                      | num     |   360 | cand. ID
#     VISCODE                  | cat/str |     9 | cand. VISITA
#     VISCODE2                 | cat/str |     7 | cand. VISITA
#     VISDATE                  | date    |   272 | cand. DATA
#     TRAILS                   | num     |     2 | DA DECIDERE
#     CUBE                     | num     |     2 | DA DECIDERE
#     CLOCKCON                 | num     |     2 | DA DECIDERE
#     CLOCKNO                  | num     |     2 | DA DECIDERE
#     CLOCKHAN                 | num     |     2 | DA DECIDERE
#     LION                     | num     |     2 | DA DECIDERE
#     RHINO                    | num     |     2 | DA DECIDERE
#     CAMEL                    | num     |     2 | DA DECIDERE
#     IMMT1W1                  | num     |     2 | DA DECIDERE
#     IMMT1W2                  | num     |     2 | DA DECIDERE
#     IMMT1W3                  | num     |     2 | DA DECIDERE
#     IMMT1W4                  | num     |     2 | DA DECIDERE
#     IMMT1W5                  | num     |     2 | DA DECIDERE
#     IMMT2W1                  | num     |     2 | DA DECIDERE
#     IMMT2W2                  | num     |     2 | DA DECIDERE
#     IMMT2W3                  | num     |     2 | DA DECIDERE
#     IMMT2W4                  | num     |     2 | DA DECIDERE
#     IMMT2W5                  | num     |     2 | DA DECIDERE
#     DIGFOR                   | num     |     2 | DA DECIDERE
#     DIGBACK                  | num     |     2 | DA DECIDERE
#     LETTERS                  | num     |    13 | DA DECIDERE
#     SERIAL1                  | num     |     2 | DA DECIDERE
#     SERIAL2                  | num     |     2 | DA DECIDERE
#     SERIAL3                  | num     |     2 | DA DECIDERE
#     SERIAL4                  | num     |     2 | DA DECIDERE
#     SERIAL5                  | num     |     2 | DA DECIDERE
#     REPEAT1                  | num     |     2 | DA DECIDERE
#     REPEAT2                  | num     |     2 | DA DECIDERE
#     FFLUENCY                 | num     |    29 | DA DECIDERE
#     ABSTRAN                  | num     |     2 | DA DECIDERE
#     ABSMEAS                  | num     |     2 | DA DECIDERE
#     DELW1                    | num     |     4 | DA DECIDERE
#     DELW2                    | num     |     4 | DA DECIDERE
#     DELW3                    | num     |     4 | DA DECIDERE
#     DELW4                    | num     |     4 | DA DECIDERE
#     DELW5                    | num     |     4 | DA DECIDERE
#     DATE                     | num     |     2 | DA DECIDERE
#     MONTH                    | num     |     2 | DA DECIDERE
#     YEAR                     | num     |     2 | DA DECIDERE
#     DAY                      | num     |     2 | DA DECIDERE
#     PLACE                    | num     |     2 | DA DECIDERE
#     CITY                     | num     |     2 | DA DECIDERE
#     MOCA                     | vuota   |     0 | DA DECIDERE
#     SOURCE                   | vuota   |     0 | DA DECIDERE
#     ID                       | num     |   478 | cand. ID
#     USERDATE                 | date    |   279 | cand. DATA
#     USERDATE2                | date    |   113 | cand. DATA
#     update_stamp             | date    |    12 | cand. DATA
# ------------------------------------------------------------------------
MOCA = DatasetConfig(
    file_code="MOCA",                          # <-- VERIFICA
    source="MOCA_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['scale'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['VISDATE', 'USERDATE2', 'update_stamp']) VERIFICA
    # 44 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['TRAILS', 'CUBE', 'CLOCKCON', 'CLOCKNO', 'CLOCKHAN', 'LION', 'RHINO', 'CAMEL', 'IMMT1W1', 'IMMT1W2', 'IMMT1W3', 'IMMT1W4', 'IMMT1W5', 'IMMT2W1', 'IMMT2W2', 'IMMT2W3', 'IMMT2W4', 'IMMT2W5', 'DIGFOR', 'DIGBACK', 'LETTERS', 'SERIAL1', 'SERIAL2', 'SERIAL3', 'SERIAL4', 'SERIAL5', 'REPEAT1', 'REPEAT2', 'FFLUENCY', 'ABSTRAN', 'ABSMEAS', 'DELW1', 'DELW2', 'DELW3', 'DELW4', 'DELW5', 'DATE', 'MONTH', 'YEAR', 'DAY', 'PLACE', 'CITY', 'MOCA', 'SOURCE']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# NEUROBAT
#   source: NEUROBAT_28Oct2025.csv   |   righe campionate: 500   |   colonne: 83
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   349 | cand. ID
#     RID                      | num     |   349 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     VISCODE2                 | cat/str |     4 | cand. VISITA
#     VISDATE                  | date    |   139 | cand. DATA
#     SOURCE                   | vuota   |     0 | DA DECIDERE
#     CLOCKCIRC                | num     |     2 | DA DECIDERE
#     CLOCKSYM                 | num     |     2 | DA DECIDERE
#     CLOCKNUM                 | num     |     2 | DA DECIDERE
#     CLOCKHAND                | num     |     2 | DA DECIDERE
#     CLOCKTIME                | num     |     2 | DA DECIDERE
#     CLOCKSCOR                | num     |     5 | DA DECIDERE
#     COPYCIRC                 | num     |     2 | DA DECIDERE
#     COPYSYM                  | num     |     3 | DA DECIDERE
#     COPYNUM                  | num     |     3 | DA DECIDERE
#     COPYHAND                 | num     |     3 | DA DECIDERE
#     COPYTIME                 | num     |     3 | DA DECIDERE
#     COPYSCOR                 | num     |     5 | DA DECIDERE
#     LMSTORY                  | vuota   |     0 | DA DECIDERE
#     LIMMTOTAL                | num     |    21 | DA DECIDERE
#     LIMMEND                  | vuota   |     0 | DA DECIDERE
#     AVTOT1                   | num     |    10 | DA DECIDERE
#     AVERR1                   | num     |     6 | DA DECIDERE
#     AVTOT2                   | num     |    13 | DA DECIDERE
#     AVERR2                   | num     |     5 | DA DECIDERE
#     AVTOT3                   | num     |    15 | DA DECIDERE
#     AVERR3                   | num     |     6 | DA DECIDERE
#     AVTOT4                   | num     |    14 | DA DECIDERE
#     AVERR4                   | num     |     6 | DA DECIDERE
#     AVTOT5                   | num     |    13 | DA DECIDERE
#     AVERR5                   | num     |     5 | DA DECIDERE
#     AVTOT6                   | num     |    17 | DA DECIDERE
#     AVERR6                   | num     |     8 | DA DECIDERE
#     AVTOTB                   | num     |    12 | DA DECIDERE
#     AVERRB                   | num     |     8 | DA DECIDERE
#     AVENDED                  | vuota   |     0 | DA DECIDERE
#     DSPANFOR                 | num     |    10 | DA DECIDERE
#     DSPANFLTH                | num     |     5 | DA DECIDERE
#     DSPANBAC                 | num     |    11 | DA DECIDERE
#     DSPANBLTH                | num     |     6 | DA DECIDERE
#     CATANIMSC                | num     |    28 | DA DECIDERE
#     CATANPERS                | num     |     8 | DA DECIDERE
#     CATANINTR                | num     |     3 | DA DECIDERE
#     CATVEGESC                | num     |    23 | DA DECIDERE
#     CATVGPERS                | num     |     6 | DA DECIDERE
#     CATVGINTR                | num     |     8 | DA DECIDERE
#     TRAASCOR                 | num     |    59 | DA DECIDERE
#     TRAAERRCOM               | num     |     4 | DA DECIDERE
#     TRAAERROM                | num     |     1 | DA DECIDERE
#     TRABSCOR                 | num     |    91 | DA DECIDERE
#     TRABERRCOM               | num     |     7 | DA DECIDERE
#     TRABERROM                | num     |    14 | DA DECIDERE
#     DIGITSCOR                | num     |    51 | DA DECIDERE
#     LDELBEGIN                | vuota   |     0 | DA DECIDERE
#     LDELTOTAL                | num     |    23 | DA DECIDERE
#     LDELCUE                  | num     |     2 | DA DECIDERE
#     BNTND                    | num     |     2 | DA DECIDERE
#     BNTSPONT                 | num     |    16 | DA DECIDERE
#     BNTSTIM                  | num     |    13 | DA DECIDERE
#     BNTCSTIM                 | num     |     5 | DA DECIDERE
#     BNTPHON                  | num     |    15 | DA DECIDERE
#     BNTCPHON                 | num     |    13 | DA DECIDERE
#     BNTTOTAL                 | num     |    15 | DA DECIDERE
#     AVDELBEGAN               | vuota   |     0 | DA DECIDERE
#     AVDEL30MIN               | num     |    16 | DA DECIDERE
#     AVDELERR1                | num     |    10 | DA DECIDERE
#     AVDELTOT                 | num     |    16 | DA DECIDERE
#     AVDELERR2                | num     |    11 | DA DECIDERE
#     ANARTERR                 | num     |    36 | DA DECIDERE
#     ANARTND                  | num     |     2 | DA DECIDERE
#     ANART                    | vuota   |     0 | DA DECIDERE
#     MINTSEMCUE               | vuota   |     0 | DA DECIDERE
#     MINTTOTAL                | vuota   |     0 | DA DECIDERE
#     MINTUNCUED               | vuota   |     0 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   144 | cand. DATA
#     USERDATE2                | date    |     2 | cand. DATA
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
NEUROBAT = DatasetConfig(
    file_code="NEUROBAT",                          # <-- VERIFICA
    source="NEUROBAT_28Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['VISDATE', 'USERDATE2', 'update_stamp']) VERIFICA
    # 69 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['SOURCE', 'CLOCKCIRC', 'CLOCKSYM', 'CLOCKNUM', 'CLOCKHAND', 'CLOCKTIME', 'CLOCKSCOR', 'COPYCIRC', 'COPYSYM', 'COPYNUM', 'COPYHAND', 'COPYTIME', 'COPYSCOR', 'LMSTORY', 'LIMMTOTAL', 'LIMMEND', 'AVTOT1', 'AVERR1', 'AVTOT2', 'AVERR2', 'AVTOT3', 'AVERR3', 'AVTOT4', 'AVERR4', 'AVTOT5', 'AVERR5', 'AVTOT6', 'AVERR6', 'AVTOTB', 'AVERRB', 'AVENDED', 'DSPANFOR', 'DSPANFLTH', 'DSPANBAC', 'DSPANBLTH', 'CATANIMSC', 'CATANPERS', 'CATANINTR', 'CATVEGESC', 'CATVGPERS', 'CATVGINTR', 'TRAASCOR', 'TRAAERRCOM', 'TRAAERROM', 'TRABSCOR', 'TRABERRCOM', 'TRABERROM', 'DIGITSCOR', 'LDELBEGIN', 'LDELTOTAL', 'LDELCUE', 'BNTND', 'BNTSPONT', 'BNTSTIM', 'BNTCSTIM', 'BNTPHON', 'BNTCPHON', 'BNTTOTAL', 'AVDELBEGAN', 'AVDEL30MIN', 'AVDELERR1', 'AVDELTOT', 'AVDELERR2', 'ANARTERR', 'ANARTND', 'ANART', 'MINTSEMCUE', 'MINTTOTAL', 'MINTUNCUED']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# NEUROPATH
#   source: NEUROPATH_06Jun2025.csv   |   righe campionate: 121   |   colonne: 164
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   121 | cand. ID
#     RID                      | num     |   121 | cand. ID
#     VISCODE2                 | cat/str |     1 | cand. VISITA
#     NPFORMMO                 | num     |    12 | DA DECIDERE
#     NPFORMDY                 | num     |    28 | DA DECIDERE
#     NPFORMYR                 | num     |    18 | DA DECIDERE
#     NPFORMDATE_DRVD          | date    |   109 | cand. DATA
#     NPDAGE                   | num     |    31 | DA DECIDERE
#     NPDODYR                  | num     |    17 | DA DECIDERE
#     NPPMIH                   | num     |    89 | DA DECIDERE
#     NPFIX                    | num     |     3 | DA DECIDERE
#     NPFIXX                   | cat/str |     1 | DA DECIDERE
#     NPWBRWT                  | num     |    73 | DA DECIDERE
#     NPWBRF                   | num     |     3 | DA DECIDERE
#     NPGRCCA                  | num     |     6 | DA DECIDERE
#     NPGRLA                   | num     |     4 | DA DECIDERE
#     NPGRHA                   | num     |     6 | DA DECIDERE
#     NPGRSNH                  | num     |     5 | DA DECIDERE
#     NPGRLCH                  | num     |     6 | DA DECIDERE
#     NPAVAS                   | num     |     6 | DA DECIDERE
#     NPTAN                    | num     |     2 | DA DECIDERE
#     NPTANX                   | vuota   |     0 | DA DECIDERE
#     NPABAN                   | num     |     1 | DA DECIDERE
#     NPABANX                  | vuota   |     0 | DA DECIDERE
#     NPASAN                   | num     |     2 | DA DECIDERE
#     NPASANX                  | vuota   |     0 | DA DECIDERE
#     NPTDPAN                  | num     |     3 | DA DECIDERE
#     NPTDPANX                 | vuota   |     0 | DA DECIDERE
#     NPHISMB                  | num     |     2 | DA DECIDERE
#     NPHISG                   | num     |     2 | DA DECIDERE
#     NPHISSS                  | num     |     1 | DA DECIDERE
#     NPHIST                   | num     |     1 | DA DECIDERE
#     NPHISO                   | num     |     2 | DA DECIDERE
#     NPHISOX                  | cat/str |     4 | DA DECIDERE
#     NPTHAL                   | num     |     6 | DA DECIDERE
#     NPBRAAK                  | num     |     7 | DA DECIDERE
#     NPNEUR                   | num     |     4 | DA DECIDERE
#     NPADNC                   | num     |     4 | DA DECIDERE
#     NPDIFF                   | num     |     4 | DA DECIDERE
#     NPAMY                    | num     |     4 | DA DECIDERE
#     NPINF                    | num     |     3 | DA DECIDERE
#     NPINF1A                  | cat/str |     4 | DA DECIDERE
#     NPINF1B                  | cat/str |     4 | DA DECIDERE
#     NPINF1D                  | cat/str |     2 | DA DECIDERE
#     NPINF1F                  | cat/str |     2 | DA DECIDERE
#     NPINF2A                  | cat/str |     3 | DA DECIDERE
#     NPINF2B                  | cat/str |     3 | DA DECIDERE
#     NPINF2D                  | vuota   |     0 | DA DECIDERE
#     NPINF2F                  | vuota   |     0 | DA DECIDERE
#     NPINF3A                  | cat/str |     4 | DA DECIDERE
#     NPINF3B                  | cat/str |     5 | DA DECIDERE
#     NPINF3D                  | cat/str |     2 | DA DECIDERE
#     NPINF3F                  | vuota   |     0 | DA DECIDERE
#     NPINF4A                  | cat/str |     3 | DA DECIDERE
#     NPINF4B                  | cat/str |     3 | DA DECIDERE
#     NPINF4D                  | vuota   |     0 | DA DECIDERE
#     NPINF4F                  | vuota   |     0 | DA DECIDERE
#     NPHEMO                   | num     |     3 | DA DECIDERE
#     NPHEMO1                  | cat/str |     3 | DA DECIDERE
#     NPHEMO2                  | cat/str |     3 | DA DECIDERE
#     NPHEMO3                  | cat/str |     2 | DA DECIDERE
#     NPOLD                    | num     |     2 | DA DECIDERE
#     NPOLD1                   | cat/str |     5 | DA DECIDERE
#     NPOLD2                   | cat/str |     4 | DA DECIDERE
#     NPOLD3                   | cat/str |     3 | DA DECIDERE
#     NPOLD4                   | cat/str |     5 | DA DECIDERE
#     NPOLDD                   | num     |     3 | DA DECIDERE
#     NPOLDD1                  | cat/str |     2 | DA DECIDERE
#     NPOLDD2                  | cat/str |     2 | DA DECIDERE
#     NPOLDD3                  | cat/str |     2 | DA DECIDERE
#     NPOLDD4                  | cat/str |     2 | DA DECIDERE
#     NPARTER                  | num     |     4 | DA DECIDERE
#     NPWMR                    | num     |     4 | DA DECIDERE
#     NPPATH                   | num     |     2 | DA DECIDERE
#     NPNEC                    | cat/str |     3 | DA DECIDERE
#     NPPATH2                  | cat/str |     2 | DA DECIDERE
#     NPPATH3                  | cat/str |     3 | DA DECIDERE
#     NPPATH4                  | cat/str |     3 | DA DECIDERE
#     NPPATH5                  | cat/str |     3 | DA DECIDERE
#     NPPATH6                  | cat/str |     3 | DA DECIDERE
#     NPPATH7                  | cat/str |     2 | DA DECIDERE
#     NPPATH8                  | cat/str |     2 | DA DECIDERE
#     NPPATH9                  | cat/str |     3 | DA DECIDERE
#     NPPATH10                 | cat/str |     2 | DA DECIDERE
#     NPPATH11                 | cat/str |     4 | DA DECIDERE
#     NPPATHO                  | cat/str |     3 | DA DECIDERE
#     NPPATHOX                 | cat/str |     5 | DA DECIDERE
#     NPLBOD                   | num     |     6 | DA DECIDERE
#     NPNLOSS                  | num     |     6 | DA DECIDERE
#     NPHIPSCL                 | num     |     5 | DA DECIDERE
#     NPTDPA                   | num     |     4 | DA DECIDERE
#     NPTDPB                   | num     |     4 | DA DECIDERE
#     NPTDPC                   | num     |     3 | DA DECIDERE
#     NPTDPD                   | num     |     3 | DA DECIDERE
#     NPTDPE                   | num     |     3 | DA DECIDERE
#     NPFTDTAU                 | num     |     2 | DA DECIDERE
#     NPPICK                   | cat/str |     2 | DA DECIDERE
#     NPFTDT2                  | cat/str |     2 | DA DECIDERE
#     NPCORT                   | cat/str |     2 | DA DECIDERE
#     NPPROG                   | cat/str |     3 | DA DECIDERE
#     NPFTDT5                  | cat/str |     3 | DA DECIDERE
#     NPFTDT6                  | cat/str |     3 | DA DECIDERE
#     NPFTDT7                  | cat/str |     3 | DA DECIDERE
#     NPFTDT8                  | cat/str |     2 | DA DECIDERE
#     NPFTDT9                  | cat/str |     3 | DA DECIDERE
#     NPFTDT10                 | cat/str |     3 | DA DECIDERE
#     NPFTDTDP                 | num     |     2 | DA DECIDERE
#     NPALSMND                 | num     |     2 | DA DECIDERE
#     NPOFTD                   | num     |     1 | DA DECIDERE
#     NPOFTD1                  | vuota   |     0 | DA DECIDERE
#     NPOFTD2                  | vuota   |     0 | DA DECIDERE
#     NPOFTD3                  | vuota   |     0 | DA DECIDERE
#     NPOFTD4                  | vuota   |     0 | DA DECIDERE
#     NPOFTD5                  | vuota   |     0 | DA DECIDERE
#     NPPDXA                   | num     |     1 | DA DECIDERE
#     NPPDXB                   | num     |     1 | DA DECIDERE
#     NPPDXC                   | num     |     1 | DA DECIDERE
#     NPPDXD                   | num     |     1 | DA DECIDERE
#     NPPDXE                   | num     |     1 | DA DECIDERE
#     NPPDXF                   | num     |     1 | DA DECIDERE
#     NPPDXG                   | num     |     1 | DA DECIDERE
#     NPPDXH                   | num     |     1 | DA DECIDERE
#     NPPDXI                   | num     |     2 | DA DECIDERE
#     NPPDXJ                   | num     |     1 | DA DECIDERE
#     NPPDXK                   | num     |     2 | DA DECIDERE
#     NPPDXL                   | num     |     1 | DA DECIDERE
#     NPPDXM                   | num     |     2 | DA DECIDERE
#     NPPDXN                   | num     |     1 | DA DECIDERE
#     NPPDXO                   | num     |     1 | DA DECIDERE
#     NPPDXP                   | num     |     3 | DA DECIDERE
#     NPPDXQ                   | num     |     3 | DA DECIDERE
#     NPPDXR                   | num     |     2 | DA DECIDERE
#     NPPDXRX                  | cat/str |    43 | DA DECIDERE
#     NPPDXS                   | num     |     2 | DA DECIDERE
#     NPPDXSX                  | cat/str |    26 | DA DECIDERE
#     NPPDXT                   | num     |     2 | DA DECIDERE
#     NPPDXTX                  | cat/str |     8 | DA DECIDERE
#     NPBNKA                   | num     |     2 | DA DECIDERE
#     NPBNKB                   | num     |     2 | DA DECIDERE
#     NPBNKC                   | num     |     2 | DA DECIDERE
#     NPBNKD                   | num     |     2 | DA DECIDERE
#     NPBNKE                   | num     |     2 | DA DECIDERE
#     NPBNKF                   | num     |     1 | DA DECIDERE
#     NPBNKG                   | num     |     3 | DA DECIDERE
#     NPFAUT                   | num     |     3 | DA DECIDERE
#     NPFAUT1                  | cat/str |     2 | DA DECIDERE
#     NPFAUT2                  | cat/str |     2 | DA DECIDERE
#     NPFAUT3                  | cat/str |     2 | DA DECIDERE
#     NPFAUT4                  | cat/str |     2 | DA DECIDERE
#     FORMVER                  | num     |     2 | DA DECIDERE
#     NPARTAG                  | cat/str |     3 | DA DECIDERE
#     NPATGSEV                 | cat/str |     4 | DA DECIDERE
#     NPATGAMY                 | cat/str |     3 | DA DECIDERE
#     NPATGAM1                 | cat/str |     4 | DA DECIDERE
#     NPATGAM2                 | cat/str |     4 | DA DECIDERE
#     NPATGAM3                 | cat/str |     5 | DA DECIDERE
#     NPATGAM4                 | cat/str |     4 | DA DECIDERE
#     NPATGAM5                 | cat/str |     4 | DA DECIDERE
#     NPATGFRN                 | cat/str |     4 | DA DECIDERE
#     NPATGFR1                 | cat/str |     3 | DA DECIDERE
#     NPATGFR2                 | cat/str |     4 | DA DECIDERE
#     NPATGFR3                 | cat/str |     4 | DA DECIDERE
#     NPATGFR4                 | cat/str |     3 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
NEUROPATH = DatasetConfig(
    file_code="NEUROPATH",                          # <-- VERIFICA
    source="NEUROPATH_06Jun2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    # date_column=?  candidati (dai valori): ['NPFORMDATE_DRVD', 'update_stamp']  <-- DECIDI
    viscode_reference="VISCODE2",
    # 159 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['NPFORMMO', 'NPFORMDY', 'NPFORMYR', 'NPDAGE', 'NPDODYR', 'NPPMIH', 'NPFIX', 'NPFIXX', 'NPWBRWT', 'NPWBRF', 'NPGRCCA', 'NPGRLA', 'NPGRHA', 'NPGRSNH', 'NPGRLCH', 'NPAVAS', 'NPTAN', 'NPTANX', 'NPABAN', 'NPABANX', 'NPASAN', 'NPASANX', 'NPTDPAN', 'NPTDPANX', 'NPHISMB', 'NPHISG', 'NPHISSS', 'NPHIST', 'NPHISO', 'NPHISOX', 'NPTHAL', 'NPBRAAK', 'NPNEUR', 'NPADNC', 'NPDIFF', 'NPAMY', 'NPINF', 'NPINF1A', 'NPINF1B', 'NPINF1D', 'NPINF1F', 'NPINF2A', 'NPINF2B', 'NPINF2D', 'NPINF2F', 'NPINF3A', 'NPINF3B', 'NPINF3D', 'NPINF3F', 'NPINF4A', 'NPINF4B', 'NPINF4D', 'NPINF4F', 'NPHEMO', 'NPHEMO1', 'NPHEMO2', 'NPHEMO3', 'NPOLD', 'NPOLD1', 'NPOLD2', 'NPOLD3', 'NPOLD4', 'NPOLDD', 'NPOLDD1', 'NPOLDD2', 'NPOLDD3', 'NPOLDD4', 'NPARTER', 'NPWMR', 'NPPATH', 'NPNEC', 'NPPATH2', 'NPPATH3', 'NPPATH4', 'NPPATH5', 'NPPATH6', 'NPPATH7', 'NPPATH8', 'NPPATH9', 'NPPATH10', 'NPPATH11', 'NPPATHO', 'NPPATHOX', 'NPLBOD', 'NPNLOSS', 'NPHIPSCL', 'NPTDPA', 'NPTDPB', 'NPTDPC', 'NPTDPD', 'NPTDPE', 'NPFTDTAU', 'NPPICK', 'NPFTDT2', 'NPCORT', 'NPPROG', 'NPFTDT5', 'NPFTDT6', 'NPFTDT7', 'NPFTDT8', 'NPFTDT9', 'NPFTDT10', 'NPFTDTDP', 'NPALSMND', 'NPOFTD', 'NPOFTD1', 'NPOFTD2', 'NPOFTD3', 'NPOFTD4', 'NPOFTD5', 'NPPDXA', 'NPPDXB', 'NPPDXC', 'NPPDXD', 'NPPDXE', 'NPPDXF', 'NPPDXG', 'NPPDXH', 'NPPDXI', 'NPPDXJ', 'NPPDXK', 'NPPDXL', 'NPPDXM', 'NPPDXN', 'NPPDXO', 'NPPDXP', 'NPPDXQ', 'NPPDXR', 'NPPDXRX', 'NPPDXS', 'NPPDXSX', 'NPPDXT', 'NPPDXTX', 'NPBNKA', 'NPBNKB', 'NPBNKC', 'NPBNKD', 'NPBNKE', 'NPBNKF', 'NPBNKG', 'NPFAUT', 'NPFAUT1', 'NPFAUT2', 'NPFAUT3', 'NPFAUT4', 'FORMVER', 'NPARTAG', 'NPATGSEV', 'NPATGAMY', 'NPATGAM1', 'NPATGAM2', 'NPATGAM3', 'NPATGAM4', 'NPATGAM5', 'NPATGFRN', 'NPATGFR1', 'NPATGFR2', 'NPATGFR3', 'NPATGFR4']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# PLASMA_ABETA_PROJECT_ADX_VUMC
#   source: PLASMA_ABETA_PROJECT_ADX_VUMC_11Aug2025.csv   |   righe campionate: 130   |   colonne: 15
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     VISCODE2                 | cat/str |     8 | cand. VISITA
#     EXAMDATE                 | date    |    99 | cand. DATA
#     DRAWTIME                 | date    |    81 | cand. DATA
#     NF_LIGHT                 | num     |   116 | DA DECIDERE
#     ABETA42                  | num     |    57 | DA DECIDERE
#     ABETA40                  | num     |   126 | DA DECIDERE
#     GFAP                     | num     |   125 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
PLASMA_ABETA_PROJECT_ADX_VUMC = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_ADX_VUMC",                          # <-- VERIFICA
    source="PLASMA_ABETA_PROJECT_ADX_VUMC_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWTIME', 'update_stamp']) VERIFICA
    # 4 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['NF_LIGHT', 'ABETA42', 'ABETA40', 'GFAP']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# PLASMA_ABETA_PROJECT_QUANTERIX
#   source: PLASMA_ABETA_PROJECT_QUANTERIX_11Aug2025.csv   |   righe campionate: 131   |   colonne: 30
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 3 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     VISCODE2                 | cat/str |     8 | cand. VISITA
#     EXAMDATE                 | date    |    99 | cand. DATA
#     DRAWTIME                 | date    |    81 | cand. DATA
#     SAMPLE_ID                | cat/str |   130 | cand. ID
#     AB1_40_RUN               | num     |     5 | DA DECIDERE
#     AB1_40_AEB_REP1          | num     |   126 | DA DECIDERE
#     AB1_40_AEB_REP2          | num     |   125 | DA DECIDERE
#     AB1_40_AVE_AEB           | num     |   128 | DA DECIDERE
#     AB1_40_CONC_REP1         | num     |   107 | DA DECIDERE
#     AB1_40_CONC_REP2         | num     |   102 | DA DECIDERE
#     AB1_40_AVE_CONC          | num     |   115 | DA DECIDERE
#     AB1_40_DILUTION_FACTOR   | num     |     1 | DA DECIDERE
#     AB1_40_DILUTION_CORRECTED_CONC | num     |   107 | DA DECIDERE
#     AB1_40_RUN_NOTES         | cat/str |     4 | DA DECIDERE
#     AB1_42_RUN               | num     |     5 | DA DECIDERE
#     AB1_42_AEB_REP1          | num     |    99 | DA DECIDERE
#     AB1_42_AEB_REP2          | num     |    99 | DA DECIDERE
#     AB1_42_AVE_AEB           | num     |   100 | DA DECIDERE
#     AB1_42_CONC_REP1         | num     |   100 | DA DECIDERE
#     AB1_42_CONC_REP2         | num     |    99 | DA DECIDERE
#     AB1_42_AVE_CONC          | num     |   105 | DA DECIDERE
#     AB1_42_DILUTION_FACTOR   | num     |     1 | DA DECIDERE
#     AB1_42_DILUTION_CORRECTED_CONC | num     |    80 | DA DECIDERE
#     AB1_42_RUN_NOTES         | cat/str |     1 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
PLASMA_ABETA_PROJECT_QUANTERIX = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_QUANTERIX",                          # <-- VERIFICA
    source="PLASMA_ABETA_PROJECT_QUANTERIX_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: ['SAMPLE_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWTIME', 'update_stamp']) VERIFICA
    # 20 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['AB1_40_RUN', 'AB1_40_AEB_REP1', 'AB1_40_AEB_REP2', 'AB1_40_AVE_AEB', 'AB1_40_CONC_REP1', 'AB1_40_CONC_REP2', 'AB1_40_AVE_CONC', 'AB1_40_DILUTION_FACTOR', 'AB1_40_DILUTION_CORRECTED_CONC', 'AB1_40_RUN_NOTES', 'AB1_42_RUN', 'AB1_42_AEB_REP1', 'AB1_42_AEB_REP2', 'AB1_42_AVE_AEB', 'AB1_42_CONC_REP1', 'AB1_42_CONC_REP2', 'AB1_42_AVE_CONC', 'AB1_42_DILUTION_FACTOR', 'AB1_42_DILUTION_CORRECTED_CONC', 'AB1_42_RUN_NOTES']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# PLASMA_ABETA_PROJECT_ROCHE
#   source: PLASMA_ABETA_PROJECT_ROCHE_11Aug2025.csv   |   righe campionate: 260   |   colonne: 13
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 3 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     VISCODE2                 | cat/str |     8 | cand. VISITA
#     EXAMDATE                 | date    |    99 | cand. DATA
#     DRAWTIME                 | date    |    81 | cand. DATA
#     STUDYID                  | cat/str |     1 | DA DECIDERE
#     RBARCODE                 | num     |   130 | DA DECIDERE
#     ASSAY                    | cat/str |     2 | DA DECIDERE
#     RESULT                   | num     |   225 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
PLASMA_ABETA_PROJECT_ROCHE = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_ROCHE",                          # <-- VERIFICA
    source="PLASMA_ABETA_PROJECT_ROCHE_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWTIME', 'update_stamp']) VERIFICA
    # 4 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['STUDYID', 'RBARCODE', 'ASSAY', 'RESULT']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# PLASMA_ABETA_PROJECT_SHIMADZU
#   source: PLASMA_ABETA_PROJECT_SHIMADZU_11Aug2025.csv   |   righe campionate: 130   |   colonne: 14
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 3 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     VISCODE2                 | cat/str |     8 | cand. VISITA
#     EXAMDATE                 | date    |    99 | cand. DATA
#     DRAWTIME                 | date    |    81 | cand. DATA
#     DATE                     | date    |     5 | cand. DATA
#     AB1_42                   | num     |   101 | DA DECIDERE
#     AB1_40                   | num     |   129 | DA DECIDERE
#     APP_669_711              | num     |   107 | DA DECIDERE
#     COMPOSITE_BIOMARKER      | num     |   125 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
PLASMA_ABETA_PROJECT_SHIMADZU = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_SHIMADZU",                          # <-- VERIFICA
    source="PLASMA_ABETA_PROJECT_SHIMADZU_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWTIME', 'DATE', 'update_stamp']) VERIFICA
    # 4 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['AB1_42', 'AB1_40', 'APP_669_711', 'COMPOSITE_BIOMARKER']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# PLASMA_ABETA_PROJECT_U_OF_GOTHENBURG
#   source: PLASMA_ABETA_PROJECT_U_OF_GOTHENBURG_11Aug2025.csv   |   righe campionate: 130   |   colonne: 16
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 4 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     VISCODE2                 | cat/str |     8 | cand. VISITA
#     EXAMDATE                 | date    |    99 | cand. DATA
#     DRAWTIME                 | date    |    81 | cand. DATA
#     NUMBER                   | num     |    67 | DA DECIDERE
#     PLATE                    | num     |     2 | DA DECIDERE
#     AB_1_37                  | num     |    73 | DA DECIDERE
#     AB_1_38                  | num     |   104 | DA DECIDERE
#     AB_1_40                  | num     |    93 | DA DECIDERE
#     AB_1_42                  | num     |    97 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
PLASMA_ABETA_PROJECT_U_OF_GOTHENBURG = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_U_OF_GOTHENBURG",                          # <-- VERIFICA
    source="PLASMA_ABETA_PROJECT_U_OF_GOTHENBURG_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWTIME', 'update_stamp']) VERIFICA
    # 6 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['NUMBER', 'PLATE', 'AB_1_37', 'AB_1_38', 'AB_1_40', 'AB_1_42']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# PLASMA_ABETA_PROJECT_WASH_U_11_05_21
#   source: PLASMA_ABETA_PROJECT_WASH_U_11_05_21_11Aug2025.csv   |   righe campionate: 130   |   colonne: 28
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   ignorate 6 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   121 | cand. ID
#     VISCODE                  | cat/str |     5 | cand. VISITA
#     VISCODE2                 | cat/str |    12 | cand. VISITA
#     EXAMDATE                 | date    |    99 | cand. DATA
#     DRAWTIME                 | date    |    81 | cand. DATA
#     FILE_NAME_NE             | cat/str |   130 | DA DECIDERE
#     LC_MS_SAMPLE_ID          | cat/str |   130 | cand. ID
#     SAMPLE_TYPE              | cat/str |     1 | DA DECIDERE
#     INJECTION                | cat/str |     3 | DA DECIDERE
#     INSTRUMENT               | cat/str |     1 | DA DECIDERE
#     BATCH                    | cat/str |     3 | DA DECIDERE
#     ASSAY                    | cat/str |     4 | DA DECIDERE
#     ASSAY_IP_PROTOCOL        | cat/str |     1 | DA DECIDERE
#     MS_RUN_DATE              | num     |     3 | DA DECIDERE
#     AB40                     | num     |   129 | DA DECIDERE
#     AB42                     | num     |   129 | DA DECIDERE
#     PLASMAAB4240             | num     |   129 | DA DECIDERE
#     STANDARDIZED_PLASMAAB42  | num     |   129 | DA DECIDERE
#     STANDARDIZED_PLASMAAB40  | num     |   129 | DA DECIDERE
#     STANDARDIZEAB42_STANDARDIZEDAB40 | num     |   129 | DA DECIDERE
#     STANDARDIZED_PLASMAAB4240 | num     |   129 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
PLASMA_ABETA_PROJECT_WASH_U_11_05_21 = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_WASH_U_11_05_21",                          # <-- VERIFICA
    source="PLASMA_ABETA_PROJECT_WASH_U_11_05_21_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: ['LC_MS_SAMPLE_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['DRAWTIME', 'update_stamp']) VERIFICA
    # 15 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['FILE_NAME_NE', 'SAMPLE_TYPE', 'INJECTION', 'INSTRUMENT', 'BATCH', 'ASSAY', 'ASSAY_IP_PROTOCOL', 'MS_RUN_DATE', 'AB40', 'AB42', 'PLASMAAB4240', 'STANDARDIZED_PLASMAAB42', 'STANDARDIZED_PLASMAAB40', 'STANDARDIZEAB42_STANDARDIZEDAB40', 'STANDARDIZED_PLASMAAB4240']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# PTDEMOG
#   source: PTDEMOG_25Jul2025.csv   |   righe campionate: 500   |   colonne: 84
#   INDIZIO categoria dal nome (NON deciso): ['cofactor']
#   ignorate 5 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   500 | cand. ID
#     RID                      | num     |   500 | cand. ID
#     VISCODE                  | cat/str |     2 | cand. VISITA
#     VISCODE2                 | cat/str |     2 | cand. VISITA
#     VISDATE                  | date    |   151 | cand. DATA
#     PTSOURCE                 | num     |     1 | DA DECIDERE
#     PTGENDER                 | num     |     2 | DA DECIDERE
#     PTDOB                    | date    |   252 | cand. DATA
#     PTDOBYY                  | num     |    36 | DA DECIDERE
#     PTHAND                   | num     |     3 | DA DECIDERE
#     PTMARRY                  | num     |     6 | DA DECIDERE
#     PTEDUCAT                 | num     |    18 | DA DECIDERE
#     PTWORKHS                 | num     |     2 | DA DECIDERE
#     PTWORK                   | vuota   |     0 | DA DECIDERE
#     PTNOTRT                  | num     |     3 | DA DECIDERE
#     PTRTYR                   | num     |    41 | DA DECIDERE
#     PTHOME                   | num     |     8 | DA DECIDERE
#     PTTLANG                  | num     |     3 | DA DECIDERE
#     PTPLANG                  | num     |     4 | DA DECIDERE
#     PTADBEG                  | num     |    12 | DA DECIDERE
#     PTCOGBEG                 | vuota   |     0 | DA DECIDERE
#     PTADDX                   | vuota   |     0 | DA DECIDERE
#     PTETHCAT                 | num     |     4 | DA DECIDERE
#     PTRACCAT                 | num     |     5 | DA DECIDERE
#     PTIDENT                  | vuota   |     0 | DA DECIDERE
#     PTORIENT                 | vuota   |     0 | DA DECIDERE
#     PTORIENTOT               | vuota   |     0 | DA DECIDERE
#     PTENGSPK                 | vuota   |     0 | DA DECIDERE
#     PTNLANG                  | vuota   |     0 | DA DECIDERE
#     PTENGSPKAGE              | vuota   |     0 | DA DECIDERE
#     PTCLANG                  | vuota   |     0 | DA DECIDERE
#     PTLANGSP                 | vuota   |     0 | DA DECIDERE
#     PTLANGWR                 | vuota   |     0 | DA DECIDERE
#     PTSPTIM                  | vuota   |     0 | DA DECIDERE
#     PTSPOTTIM                | vuota   |     0 | DA DECIDERE
#     PTLANGPR1                | vuota   |     0 | DA DECIDERE
#     PTLANGSP1                | vuota   |     0 | DA DECIDERE
#     PTLANGRD1                | vuota   |     0 | DA DECIDERE
#     PTLANGWR1                | vuota   |     0 | DA DECIDERE
#     PTLANGUN1                | vuota   |     0 | DA DECIDERE
#     PTLANGPR2                | vuota   |     0 | DA DECIDERE
#     PTLANGSP2                | vuota   |     0 | DA DECIDERE
#     PTLANGRD2                | vuota   |     0 | DA DECIDERE
#     PTLANGWR2                | vuota   |     0 | DA DECIDERE
#     PTLANGUN2                | vuota   |     0 | DA DECIDERE
#     PTLANGPR3                | vuota   |     0 | DA DECIDERE
#     PTLANGSP3                | vuota   |     0 | DA DECIDERE
#     PTLANGRD3                | vuota   |     0 | DA DECIDERE
#     PTLANGWR3                | vuota   |     0 | DA DECIDERE
#     PTLANGUN3                | vuota   |     0 | DA DECIDERE
#     PTLANGPR4                | vuota   |     0 | DA DECIDERE
#     PTLANGSP4                | vuota   |     0 | DA DECIDERE
#     PTLANGRD4                | vuota   |     0 | DA DECIDERE
#     PTLANGWR4                | vuota   |     0 | DA DECIDERE
#     PTLANGUN4                | vuota   |     0 | DA DECIDERE
#     PTLANGPR5                | vuota   |     0 | DA DECIDERE
#     PTLANGSP5                | vuota   |     0 | DA DECIDERE
#     PTLANGRD5                | vuota   |     0 | DA DECIDERE
#     PTLANGWR5                | vuota   |     0 | DA DECIDERE
#     PTLANGUN5                | vuota   |     0 | DA DECIDERE
#     PTLANGPR6                | vuota   |     0 | DA DECIDERE
#     PTLANGSP6                | vuota   |     0 | DA DECIDERE
#     PTLANGRD6                | vuota   |     0 | DA DECIDERE
#     PTLANGWR6                | vuota   |     0 | DA DECIDERE
#     PTLANGUN6                | vuota   |     0 | DA DECIDERE
#     PTLANGTTL                | vuota   |     0 | DA DECIDERE
#     PTETHCATH                | vuota   |     0 | DA DECIDERE
#     PTASIAN                  | vuota   |     0 | DA DECIDERE
#     PTOPI                    | vuota   |     0 | DA DECIDERE
#     PTBORN                   | vuota   |     0 | DA DECIDERE
#     PTBIRPL                  | vuota   |     0 | DA DECIDERE
#     PTIMMAGE                 | vuota   |     0 | DA DECIDERE
#     PTIMMWHY                 | vuota   |     0 | DA DECIDERE
#     PTBIRPR                  | vuota   |     0 | DA DECIDERE
#     PTBIRGR                  | vuota   |     0 | DA DECIDERE
#     ID                       | num     |   500 | cand. ID
#     USERDATE                 | date    |   149 | cand. DATA
#     USERDATE2                | date    |    25 | cand. DATA
#     update_stamp             | date    |   172 | cand. DATA
# ------------------------------------------------------------------------
PTDEMOG = DatasetConfig(
    file_code="PTDEMOG",                          # <-- VERIFICA
    source="PTDEMOG_25Jul2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['cofactor'])
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'ID']) VERIFICA
    date_column="USERDATE",          # preferenza ADNI (alt: ['VISDATE', 'PTDOB', 'USERDATE2', 'update_stamp']) VERIFICA
    # 69 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['PTSOURCE', 'PTGENDER', 'PTDOBYY', 'PTHAND', 'PTMARRY', 'PTEDUCAT', 'PTWORKHS', 'PTWORK', 'PTNOTRT', 'PTRTYR', 'PTHOME', 'PTTLANG', 'PTPLANG', 'PTADBEG', 'PTCOGBEG', 'PTADDX', 'PTETHCAT', 'PTRACCAT', 'PTIDENT', 'PTORIENT', 'PTORIENTOT', 'PTENGSPK', 'PTNLANG', 'PTENGSPKAGE', 'PTCLANG', 'PTLANGSP', 'PTLANGWR', 'PTSPTIM', 'PTSPOTTIM', 'PTLANGPR1', 'PTLANGSP1', 'PTLANGRD1', 'PTLANGWR1', 'PTLANGUN1', 'PTLANGPR2', 'PTLANGSP2', 'PTLANGRD2', 'PTLANGWR2', 'PTLANGUN2', 'PTLANGPR3', 'PTLANGSP3', 'PTLANGRD3', 'PTLANGWR3', 'PTLANGUN3', 'PTLANGPR4', 'PTLANGSP4', 'PTLANGRD4', 'PTLANGWR4', 'PTLANGUN4', 'PTLANGPR5', 'PTLANGSP5', 'PTLANGRD5', 'PTLANGWR5', 'PTLANGUN5', 'PTLANGPR6', 'PTLANGSP6', 'PTLANGRD6', 'PTLANGWR6', 'PTLANGUN6', 'PTLANGTTL', 'PTETHCATH', 'PTASIAN', 'PTOPI', 'PTBORN', 'PTBIRPL', 'PTIMMAGE', 'PTIMMWHY', 'PTBIRPR', 'PTBIRGR']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# RMT_APOERES
#   source: RMT_APOERES_28Oct2025.csv   |   righe campionate: 500   |   colonne: 4
#   INDIZIO categoria dal nome (NON deciso): ['cofactor']
#   ignorate 1 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     ADNIOnlineID             | cat/str |   500 | DA DECIDERE
#     GENOTYPE                 | cat/str |     6 | DA DECIDERE
#     update_stamp             | date    |     5 | cand. DATA
# ------------------------------------------------------------------------
RMT_APOERES = DatasetConfig(
    file_code="RMT_APOERES",                          # <-- VERIFICA
    source="RMT_APOERES_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['cofactor'])
    # id_column=?  candidati: NESSUNO  <-- DECIDI
    date_column="update_stamp",                  # rilevato dai valori, VERIFICA
    # 2 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['ADNIOnlineID', 'GENOTYPE']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# RMT_ECOG12PT
#   source: RMT_ECOG12PT_04Nov2025.csv   |   righe campionate: 500   |   colonne: 21
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RMT_PHASE                | cat/str |     1 | DA DECIDERE
#     ADNIOnlineID             | cat/str |   332 | DA DECIDERE
#     PTID                     | cat/str |    77 | cand. ID
#     RMT_Timepoint            | cat/str |     3 | DA DECIDERE
#     RMT_StatusDate           | date    |   248 | cand. DATA
#     RMT_CONCERN              | num     |     3 | DA DECIDERE
#     RMT_MEMREF               | num     |     3 | DA DECIDERE
#     RMT_ecogpt_Duration      | num     |   219 | DA DECIDERE
#     RMT_ecogpt1              | num     |     5 | DA DECIDERE
#     RMT_ecogpt2              | num     |     5 | DA DECIDERE
#     RMT_ecogpt3              | num     |     5 | DA DECIDERE
#     RMT_ecogpt4              | num     |     5 | DA DECIDERE
#     RMT_ecogpt5              | num     |     5 | DA DECIDERE
#     RMT_ecogpt6              | num     |     5 | DA DECIDERE
#     RMT_ecogpt7              | num     |     5 | DA DECIDERE
#     RMT_ecogpt8              | num     |     5 | DA DECIDERE
#     RMT_ecogpt9              | num     |     5 | DA DECIDERE
#     RMT_ecogpt10             | num     |     5 | DA DECIDERE
#     RMT_ecogpt11             | num     |     5 | DA DECIDERE
#     RMT_ecogpt12             | num     |     5 | DA DECIDERE
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
RMT_ECOG12PT = DatasetConfig(
    file_code="RMT_ECOG12PT",                          # <-- VERIFICA
    source="RMT_ECOG12PT_04Nov2025.csv",
    category=None,                              # <-- DECIDI
    id_column="PTID",                      # rilevato, VERIFICA
    # date_column=?  candidati (dai valori): ['RMT_StatusDate', 'update_stamp']  <-- DECIDI
    # 18 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['RMT_PHASE', 'ADNIOnlineID', 'RMT_Timepoint', 'RMT_CONCERN', 'RMT_MEMREF', 'RMT_ecogpt_Duration', 'RMT_ecogpt1', 'RMT_ecogpt2', 'RMT_ecogpt3', 'RMT_ecogpt4', 'RMT_ecogpt5', 'RMT_ecogpt6', 'RMT_ecogpt7', 'RMT_ecogpt8', 'RMT_ecogpt9', 'RMT_ecogpt10', 'RMT_ecogpt11', 'RMT_ecogpt12']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# RMT_ECOG12SP
#   source: RMT_ECOG12SP_04Nov2025.csv   |   righe campionate: 500   |   colonne: 21
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RMT_PHASE                | cat/str |     1 | DA DECIDERE
#     ADNIOnlineID             | cat/str |   380 | DA DECIDERE
#     PTID                     | cat/str |    66 | cand. ID
#     RMT_Timepoint            | cat/str |     3 | DA DECIDERE
#     RMT_StatusDate           | date    |   237 | cand. DATA
#     RMT_SP_CONCERN           | num     |     3 | DA DECIDERE
#     RMT_SP_MEMREF            | num     |     3 | DA DECIDERE
#     RMT_ecogsp_Duration      | num     |   206 | DA DECIDERE
#     RMT_ecogsp1              | num     |     5 | DA DECIDERE
#     RMT_ecogsp2              | num     |     5 | DA DECIDERE
#     RMT_ecogsp3              | num     |     5 | DA DECIDERE
#     RMT_ecogsp4              | num     |     5 | DA DECIDERE
#     RMT_ecogsp5              | num     |     5 | DA DECIDERE
#     RMT_ecogsp6              | num     |     4 | DA DECIDERE
#     RMT_ecogsp7              | num     |     5 | DA DECIDERE
#     RMT_ecogsp8              | num     |     5 | DA DECIDERE
#     RMT_ecogsp9              | num     |     5 | DA DECIDERE
#     RMT_ecogsp10             | num     |     5 | DA DECIDERE
#     RMT_ecogsp11             | num     |     5 | DA DECIDERE
#     RMT_ecogsp12             | num     |     5 | DA DECIDERE
#     update_stamp             | date    |     4 | cand. DATA
# ------------------------------------------------------------------------
RMT_ECOG12SP = DatasetConfig(
    file_code="RMT_ECOG12SP",                          # <-- VERIFICA
    source="RMT_ECOG12SP_04Nov2025.csv",
    category=None,                              # <-- DECIDI
    id_column="PTID",                      # rilevato, VERIFICA
    # date_column=?  candidati (dai valori): ['RMT_StatusDate', 'update_stamp']  <-- DECIDI
    # 18 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['RMT_PHASE', 'ADNIOnlineID', 'RMT_Timepoint', 'RMT_SP_CONCERN', 'RMT_SP_MEMREF', 'RMT_ecogsp_Duration', 'RMT_ecogsp1', 'RMT_ecogsp2', 'RMT_ecogsp3', 'RMT_ecogsp4', 'RMT_ecogsp5', 'RMT_ecogsp6', 'RMT_ecogsp7', 'RMT_ecogsp8', 'RMT_ecogsp9', 'RMT_ecogsp10', 'RMT_ecogsp11', 'RMT_ecogsp12']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# RMT_PTDEMOG
#   source: RMT_PTDEMOG_04Nov2025.csv   |   righe campionate: 500   |   colonne: 23
#   INDIZIO categoria dal nome (NON deciso): ['cofactor']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RMT_PHASE                | cat/str |     1 | DA DECIDERE
#     ADNIOnlineID             | cat/str |   499 | DA DECIDERE
#     PTID                     | cat/str |    18 | cand. ID
#     RMT_Timepoint            | cat/str |     3 | DA DECIDERE
#     RMT_StatusDate           | date    |   242 | cand. DATA
#     Age_Baseline             | num     |    33 | DA DECIDERE
#     Gender                   | num     |     3 | DA DECIDERE
#     LatinoEthnicity          | num     |     3 | DA DECIDERE
#     Latino_MX                | num     |     2 | DA DECIDERE
#     Latino_PR                | num     |     2 | DA DECIDERE
#     Latino_CB                | num     |     2 | DA DECIDERE
#     Latino_Other             | num     |     2 | DA DECIDERE
#     Race_AmerIndian          | num     |     2 | DA DECIDERE
#     Race_Asian               | num     |     2 | DA DECIDERE
#     Race_AfricanAmerican     | num     |     2 | DA DECIDERE
#     Race_PacificIslander     | num     |     2 | DA DECIDERE
#     Race_White               | num     |     2 | DA DECIDERE
#     Race_Unknown             | num     |     2 | DA DECIDERE
#     Race_PreferNotSay        | num     |     2 | DA DECIDERE
#     RMT_Education            | num     |     9 | DA DECIDERE
#     RMT_ADI_NATRANK_v2021    | num     |    94 | DA DECIDERE
#     RMT_ADI_STATERANK_v2021  | num     |    10 | DA DECIDERE
#     update_stamp             | date    |     4 | cand. DATA
# ------------------------------------------------------------------------
RMT_PTDEMOG = DatasetConfig(
    file_code="RMT_PTDEMOG",                          # <-- VERIFICA
    source="RMT_PTDEMOG_04Nov2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['cofactor'])
    id_column="PTID",                      # rilevato, VERIFICA
    # date_column=?  candidati (dai valori): ['RMT_StatusDate', 'update_stamp']  <-- DECIDI
    # 20 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['RMT_PHASE', 'ADNIOnlineID', 'RMT_Timepoint', 'Age_Baseline', 'Gender', 'LatinoEthnicity', 'Latino_MX', 'Latino_PR', 'Latino_CB', 'Latino_Other', 'Race_AmerIndian', 'Race_Asian', 'Race_AfricanAmerican', 'Race_PacificIslander', 'Race_White', 'Race_Unknown', 'Race_PreferNotSay', 'RMT_Education', 'RMT_ADI_NATRANK_v2021', 'RMT_ADI_STATERANK_v2021']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# RMT_SCREENING
#   source: RMT_Screening_04Nov2025.csv   |   righe campionate: 500   |   colonne: 26
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RMT_PHASE                | cat/str |     1 | DA DECIDERE
#     ADNIOnlineID             | cat/str |   500 | DA DECIDERE
#     PTID                     | cat/str |    29 | cand. ID
#     RMT_Timepoint            | cat/str |     2 | DA DECIDERE
#     RMT_StatusDate           | date    |   179 | cand. DATA
#     RMT_MCI_Dx               | num     |     4 | DA DECIDERE
#     RMT_AD_Dx                | num     |     4 | DA DECIDERE
#     RMT_DEM_Dx               | num     |     4 | DA DECIDERE
#     RMT_CImed                | num     |     3 | DA DECIDERE
#     RMT_FamAD                | num     |     4 | DA DECIDERE
#     RMT_NursHm               | num     |     2 | DA DECIDERE
#     RMT_MntlHlth             | num     |     3 | DA DECIDERE
#     RMT_BrainCndtn           | num     |     3 | DA DECIDERE
#     RMT_AlchlDrug            | num     |     3 | DA DECIDERE
#     RMT_Metal                | num     |     2 | DA DECIDERE
#     RMT_Metal_rplc           | num     |     2 | DA DECIDERE
#     RMT_Metal_other          | num     |     2 | DA DECIDERE
#     RMT_MemStudy             | num     |     3 | DA DECIDERE
#     RMT_MRIPET               | num     |     3 | DA DECIDERE
#     RMT_Clausphba            | num     |     4 | DA DECIDERE
#     RMT_BLDwill              | num     |     3 | DA DECIDERE
#     RMT_Web                  | num     |     2 | DA DECIDERE
#     RMT_Device               | num     |     2 | DA DECIDERE
#     Referral_BLD             | num     |     2 | DA DECIDERE
#     Referral_CLIN            | num     |     2 | DA DECIDERE
#     update_stamp             | date    |     3 | cand. DATA
# ------------------------------------------------------------------------
RMT_SCREENING = DatasetConfig(
    file_code="RMT_Screening",                          # <-- VERIFICA
    source="RMT_Screening_04Nov2025.csv",
    category=None,                              # <-- DECIDI
    id_column="PTID",                      # rilevato, VERIFICA
    # date_column=?  candidati (dai valori): ['RMT_StatusDate', 'update_stamp']  <-- DECIDI
    # 23 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['RMT_PHASE', 'ADNIOnlineID', 'RMT_Timepoint', 'RMT_MCI_Dx', 'RMT_AD_Dx', 'RMT_DEM_Dx', 'RMT_CImed', 'RMT_FamAD', 'RMT_NursHm', 'RMT_MntlHlth', 'RMT_BrainCndtn', 'RMT_AlchlDrug', 'RMT_Metal', 'RMT_Metal_rplc', 'RMT_Metal_other', 'RMT_MemStudy', 'RMT_MRIPET', 'RMT_Clausphba', 'RMT_BLDwill', 'RMT_Web', 'RMT_Device', 'Referral_BLD', 'Referral_CLIN']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# SALADAX_BIOMEDICAL
#   source: SALADAX_BIOMEDICAL_11Aug2025.csv   |   righe campionate: 393   |   colonne: 10
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   262 | cand. ID
#     EXAMDATE                 | date    |   306 | cand. DATA
#     PTID                     | cat/str |   262 | cand. ID
#     VISCODE2                 | cat/str |     2 | cand. VISITA
#     SAMPLE_ID                | cat/str |   375 | cand. ID
#     TESTINGDATE              | date    |     3 | cand. DATA
#     BIOFLUID                 | cat/str |     1 | DA DECIDERE
#     ABETA42                  | num     |   279 | DA DECIDERE
#     TOTALTAU                 | num     |   260 | DA DECIDERE
#     UNITS                    | cat/str |     1 | DA DECIDERE
# ------------------------------------------------------------------------
SALADAX_BIOMEDICAL = DatasetConfig(
    file_code="SALADAX_BIOMEDICAL",                          # <-- VERIFICA
    source="SALADAX_BIOMEDICAL_11Aug2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID', 'SAMPLE_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['TESTINGDATE']) VERIFICA
    viscode_reference="VISCODE2",
    # 4 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['BIOFLUID', 'ABETA42', 'TOTALTAU', 'UNITS']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCBERKELEY_AMY_6MM
#   source: UCBERKELEY_AMY_6MM_28Oct2025.csv   |   righe campionate: 500   |   colonne: 344
#   INDIZIO categoria dal nome (NON deciso): ['pet']
#   ignorate 3 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   286 | cand. ID
#     RID                      | num     |   286 | cand. ID
#     VISCODE                  | cat/str |     6 | cand. VISITA
#     VISCODE2                 | cat/str |    14 | cand. VISITA
#     SCANDATE                 | date    |   347 | cand. DATA
#     PROCESSDATE              | date    |    33 | cand. DATA
#     IMAGE_RESOLUTION         | cat/str |     2 | DA DECIDERE
#     TRACER                   | cat/str |     1 | DA DECIDERE
#     TRACER_SUVR_WARNING      | cat/str |     1 | DA DECIDERE
#     AMYLOID_STATUS           | num     |     2 | DA DECIDERE
#     AMYLOID_STATUS_COMPOSITE_REF | num     |     2 | DA DECIDERE
#     CENTILOIDS               | num     |   133 | DA DECIDERE
#     SUMMARY_SUVR             | num     |   326 | DA DECIDERE
#     SUMMARY_VOLUME           | num     |   462 | DA DECIDERE
#     WHOLECEREBELLUM_SUVR     | num     |     1 | DA DECIDERE
#     WHOLECEREBELLUM_VOLUME   | num     |   459 | DA DECIDERE
#     COMPOSITE_REF_SUVR       | num     |   227 | DA DECIDERE
#     COMPOSITE_REF_VOLUME     | num     |   462 | DA DECIDERE
#     CEREBELLUM_CORTEX_SUVR   | num     |    99 | DA DECIDERE
#     CEREBELLUM_CORTEX_VOLUME | num     |   461 | DA DECIDERE
#     ERODED_SUBCORTICALWM_SUVR | num     |   316 | DA DECIDERE
#     ERODED_SUBCORTICALWM_VOLUME | num     |   460 | DA DECIDERE
#     BRAINSTEM_SUVR           | num     |   264 | DA DECIDERE
#     BRAINSTEM_VOLUME         | num     |   451 | DA DECIDERE
#     CC_ANTERIOR_SUVR         | num     |   331 | DA DECIDERE
#     CC_ANTERIOR_VOLUME       | num     |   322 | DA DECIDERE
#     CC_CENTRAL_SUVR          | num     |   331 | DA DECIDERE
#     CC_CENTRAL_VOLUME        | num     |   265 | DA DECIDERE
#     CC_MID_ANTERIOR_SUVR     | num     |   346 | DA DECIDERE
#     CC_MID_ANTERIOR_VOLUME   | num     |   267 | DA DECIDERE
#     CC_MID_POSTERIOR_SUVR    | num     |   329 | DA DECIDERE
#     CC_MID_POSTERIOR_VOLUME  | num     |   282 | DA DECIDERE
#     CC_POSTERIOR_SUVR        | num     |   340 | DA DECIDERE
#     CC_POSTERIOR_VOLUME      | num     |   327 | DA DECIDERE
#     CSF_SUVR                 | num     |   287 | DA DECIDERE
#     CSF_VOLUME               | num     |   378 | DA DECIDERE
#     VENTRICLE_3RD_SUVR       | num     |   282 | DA DECIDERE
#     VENTRICLE_3RD_VOLUME     | num     |   426 | DA DECIDERE
#     VENTRICLE_4TH_SUVR       | num     |   252 | DA DECIDERE
#     VENTRICLE_4TH_VOLUME     | num     |   407 | DA DECIDERE
#     VENTRICLE_5TH_SUVR       | num     |     3 | DA DECIDERE
#     VENTRICLE_5TH_VOLUME     | num     |     2 | DA DECIDERE
#     WM_HYPOINTENSITIES_SUVR  | num     |   313 | DA DECIDERE
#     WM_HYPOINTENSITIES_VOLUME | num     |   450 | DA DECIDERE
#     NON_WM_HYPOINTENSITIES_SUVR | num     |    41 | DA DECIDERE
#     NON_WM_HYPOINTENSITIES_VOLUME | num     |    12 | DA DECIDERE
#     CTX_BANKSSTS_SUVR        | num     |   328 | DA DECIDERE
#     CTX_BANKSSTS_VOLUME      | num     |   426 | DA DECIDERE
#     CTX_CAUDALANTERIORCINGULATE_SUVR | num     |   343 | DA DECIDERE
#     CTX_CAUDALANTERIORCINGULATE_VOLUME | num     |   418 | DA DECIDERE
#     CTX_CAUDALMIDDLEFRONTAL_SUVR | num     |   316 | DA DECIDERE
#     CTX_CAUDALMIDDLEFRONTAL_VOLUME | num     |   443 | DA DECIDERE
#     CTX_CUNEUS_SUVR          | num     |   292 | DA DECIDERE
#     CTX_CUNEUS_VOLUME        | num     |   431 | DA DECIDERE
#     CTX_ENTORHINAL_SUVR      | num     |   280 | DA DECIDERE
#     CTX_ENTORHINAL_VOLUME    | num     |   423 | DA DECIDERE
#     CTX_FRONTALPOLE_SUVR     | num     |   354 | DA DECIDERE
#     CTX_FRONTALPOLE_VOLUME   | num     |   377 | DA DECIDERE
#     CTX_FUSIFORM_SUVR        | num     |   318 | DA DECIDERE
#     CTX_FUSIFORM_VOLUME      | num     |   452 | DA DECIDERE
#     CTX_INFERIORPARIETAL_SUVR | num     |   325 | DA DECIDERE
#     CTX_INFERIORPARIETAL_VOLUME | num     |   452 | DA DECIDERE
#     CTX_INFERIORTEMPORAL_SUVR | num     |   326 | DA DECIDERE
#     CTX_INFERIORTEMPORAL_VOLUME | num     |   450 | DA DECIDERE
#     CTX_INSULA_SUVR          | num     |   305 | DA DECIDERE
#     CTX_INSULA_VOLUME        | num     |   440 | DA DECIDERE
#     CTX_ISTHMUSCINGULATE_SUVR | num     |   338 | DA DECIDERE
#     CTX_ISTHMUSCINGULATE_VOLUME | num     |   429 | DA DECIDERE
#     CTX_LATERALOCCIPITAL_SUVR | num     |   320 | DA DECIDERE
#     CTX_LATERALOCCIPITAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_LATERALORBITOFRONTAL_SUVR | num     |   321 | DA DECIDERE
#     CTX_LATERALORBITOFRONTAL_VOLUME | num     |   445 | DA DECIDERE
#     CTX_LINGUAL_SUVR         | num     |   279 | DA DECIDERE
#     CTX_LINGUAL_VOLUME       | num     |   439 | DA DECIDERE
#     CTX_MEDIALORBITOFRONTAL_SUVR | num     |   328 | DA DECIDERE
#     CTX_MEDIALORBITOFRONTAL_VOLUME | num     |   447 | DA DECIDERE
#     CTX_MIDDLETEMPORAL_SUVR  | num     |   318 | DA DECIDERE
#     CTX_MIDDLETEMPORAL_VOLUME | num     |   449 | DA DECIDERE
#     CTX_PARACENTRAL_SUVR     | num     |   305 | DA DECIDERE
#     CTX_PARACENTRAL_VOLUME   | num     |   432 | DA DECIDERE
#     CTX_PARAHIPPOCAMPAL_SUVR | num     |   281 | DA DECIDERE
#     CTX_PARAHIPPOCAMPAL_VOLUME | num     |   406 | DA DECIDERE
#     CTX_PARSOPERCULARIS_SUVR | num     |   316 | DA DECIDERE
#     CTX_PARSOPERCULARIS_VOLUME | num     |   439 | DA DECIDERE
#     CTX_PARSORBITALIS_SUVR   | num     |   345 | DA DECIDERE
#     CTX_PARSORBITALIS_VOLUME | num     |   415 | DA DECIDERE
#     CTX_PARSTRIANGULARIS_SUVR | num     |   337 | DA DECIDERE
#     CTX_PARSTRIANGULARIS_VOLUME | num     |   429 | DA DECIDERE
#     CTX_PERICALCARINE_SUVR   | num     |   302 | DA DECIDERE
#     CTX_PERICALCARINE_VOLUME | num     |   422 | DA DECIDERE
#     CTX_POSTCENTRAL_SUVR     | num     |   288 | DA DECIDERE
#     CTX_POSTCENTRAL_VOLUME   | num     |   450 | DA DECIDERE
#     CTX_POSTERIORCINGULATE_SUVR | num     |   335 | DA DECIDERE
#     CTX_POSTERIORCINGULATE_VOLUME | num     |   429 | DA DECIDERE
#     CTX_PRECENTRAL_SUVR      | num     |   288 | DA DECIDERE
#     CTX_PRECENTRAL_VOLUME    | num     |   449 | DA DECIDERE
#     CTX_PRECUNEUS_SUVR       | num     |   324 | DA DECIDERE
#     CTX_PRECUNEUS_VOLUME     | num     |   450 | DA DECIDERE
#     CTX_ROSTRALANTERIORCINGULATE_SUVR | num     |   340 | DA DECIDERE
#     CTX_ROSTRALANTERIORCINGULATE_VOLUME | num     |   427 | DA DECIDERE
#     CTX_ROSTRALMIDDLEFRONTAL_SUVR | num     |   341 | DA DECIDERE
#     CTX_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   453 | DA DECIDERE
#     CTX_SUPERIORFRONTAL_SUVR | num     |   322 | DA DECIDERE
#     CTX_SUPERIORFRONTAL_VOLUME | num     |   457 | DA DECIDERE
#     CTX_SUPERIORPARIETAL_SUVR | num     |   309 | DA DECIDERE
#     CTX_SUPERIORPARIETAL_VOLUME | num     |   445 | DA DECIDERE
#     CTX_SUPERIORTEMPORAL_SUVR | num     |   306 | DA DECIDERE
#     CTX_SUPERIORTEMPORAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_SUPRAMARGINAL_SUVR   | num     |   320 | DA DECIDERE
#     CTX_SUPRAMARGINAL_VOLUME | num     |   450 | DA DECIDERE
#     CTX_TEMPORALPOLE_SUVR    | num     |   309 | DA DECIDERE
#     CTX_TEMPORALPOLE_VOLUME  | num     |   432 | DA DECIDERE
#     CTX_TRANSVERSETEMPORAL_SUVR | num     |   303 | DA DECIDERE
#     CTX_TRANSVERSETEMPORAL_VOLUME | num     |   366 | DA DECIDERE
#     ACCUMBENS_AREA_SUVR      | num     |   350 | DA DECIDERE
#     ACCUMBENS_AREA_VOLUME    | num     |   333 | DA DECIDERE
#     AMYGDALA_SUVR            | num     |   285 | DA DECIDERE
#     AMYGDALA_VOLUME          | num     |   411 | DA DECIDERE
#     CAUDATE_SUVR             | num     |   305 | DA DECIDERE
#     CAUDATE_VOLUME           | num     |   429 | DA DECIDERE
#     CEREBELLUM_WHITE_MATTER_SUVR | num     |   274 | DA DECIDERE
#     CEREBELLUM_WHITE_MATTER_VOLUME | num     |   451 | DA DECIDERE
#     CEREBRAL_WHITE_MATTER_SUVR | num     |   321 | DA DECIDERE
#     CEREBRAL_WHITE_MATTER_VOLUME | num     |   462 | DA DECIDERE
#     CHOROID_PLEXUS_SUVR      | num     |   307 | DA DECIDERE
#     CHOROID_PLEXUS_VOLUME    | num     |   401 | DA DECIDERE
#     HIPPOCAMPUS_SUVR         | num     |   248 | DA DECIDERE
#     HIPPOCAMPUS_VOLUME       | num     |   433 | DA DECIDERE
#     OPTIC_CHIASM_SUVR        | num     |   268 | DA DECIDERE
#     OPTIC_CHIASM_VOLUME      | num     |   151 | DA DECIDERE
#     INF_LAT_VENT_SUVR        | num     |   310 | DA DECIDERE
#     INF_LAT_VENT_VOLUME      | num     |   429 | DA DECIDERE
#     LATERAL_VENTRICLE_SUVR   | num     |   321 | DA DECIDERE
#     LATERAL_VENTRICLE_VOLUME | num     |   460 | DA DECIDERE
#     PALLIDUM_SUVR            | num     |   289 | DA DECIDERE
#     PALLIDUM_VOLUME          | num     |   411 | DA DECIDERE
#     PUTAMEN_SUVR             | num     |   313 | DA DECIDERE
#     PUTAMEN_VOLUME           | num     |   442 | DA DECIDERE
#     THALAMUS_PROPER_SUVR     | num     |   284 | DA DECIDERE
#     THALAMUS_PROPER_VOLUME   | num     |   449 | DA DECIDERE
#     VENTRALDC_SUVR           | num     |   262 | DA DECIDERE
#     VENTRALDC_VOLUME         | num     |   422 | DA DECIDERE
#     VESSEL_SUVR              | num     |   333 | DA DECIDERE
#     VESSEL_VOLUME            | num     |   136 | DA DECIDERE
#     CTX_LH_BANKSSTS_SUVR     | num     |   338 | DA DECIDERE
#     CTX_LH_BANKSSTS_VOLUME   | num     |   388 | DA DECIDERE
#     CTX_LH_CAUDALANTERIORCINGULATE_SUVR | num     |   345 | DA DECIDERE
#     CTX_LH_CAUDALANTERIORCINGULATE_VOLUME | num     |   403 | DA DECIDERE
#     CTX_LH_CAUDALMIDDLEFRONTAL_SUVR | num     |   331 | DA DECIDERE
#     CTX_LH_CAUDALMIDDLEFRONTAL_VOLUME | num     |   429 | DA DECIDERE
#     CTX_LH_CUNEUS_SUVR       | num     |   280 | DA DECIDERE
#     CTX_LH_CUNEUS_VOLUME     | num     |   408 | DA DECIDERE
#     CTX_LH_ENTORHINAL_SUVR   | num     |   281 | DA DECIDERE
#     CTX_LH_ENTORHINAL_VOLUME | num     |   401 | DA DECIDERE
#     CTX_LH_FRONTALPOLE_SUVR  | num     |   367 | DA DECIDERE
#     CTX_LH_FRONTALPOLE_VOLUME | num     |   322 | DA DECIDERE
#     CTX_LH_FUSIFORM_SUVR     | num     |   313 | DA DECIDERE
#     CTX_LH_FUSIFORM_VOLUME   | num     |   448 | DA DECIDERE
#     CTX_LH_INFERIORPARIETAL_SUVR | num     |   318 | DA DECIDERE
#     CTX_LH_INFERIORPARIETAL_VOLUME | num     |   448 | DA DECIDERE
#     CTX_LH_INFERIORTEMPORAL_SUVR | num     |   327 | DA DECIDERE
#     CTX_LH_INFERIORTEMPORAL_VOLUME | num     |   442 | DA DECIDERE
#     CTX_LH_INSULA_SUVR       | num     |   307 | DA DECIDERE
#     CTX_LH_INSULA_VOLUME     | num     |   436 | DA DECIDERE
#     CTX_LH_ISTHMUSCINGULATE_SUVR | num     |   324 | DA DECIDERE
#     CTX_LH_ISTHMUSCINGULATE_VOLUME | num     |   404 | DA DECIDERE
#     CTX_LH_LATERALOCCIPITAL_SUVR | num     |   304 | DA DECIDERE
#     CTX_LH_LATERALOCCIPITAL_VOLUME | num     |   443 | DA DECIDERE
#     CTX_LH_LATERALORBITOFRONTAL_SUVR | num     |   335 | DA DECIDERE
#     CTX_LH_LATERALORBITOFRONTAL_VOLUME | num     |   419 | DA DECIDERE
#     CTX_LH_LINGUAL_SUVR      | num     |   273 | DA DECIDERE
#     CTX_LH_LINGUAL_VOLUME    | num     |   437 | DA DECIDERE
#     CTX_LH_MEDIALORBITOFRONTAL_SUVR | num     |   329 | DA DECIDERE
#     CTX_LH_MEDIALORBITOFRONTAL_VOLUME | num     |   414 | DA DECIDERE
#     CTX_LH_MIDDLETEMPORAL_SUVR | num     |   324 | DA DECIDERE
#     CTX_LH_MIDDLETEMPORAL_VOLUME | num     |   444 | DA DECIDERE
#     CTX_LH_PARACENTRAL_SUVR  | num     |   314 | DA DECIDERE
#     CTX_LH_PARACENTRAL_VOLUME | num     |   411 | DA DECIDERE
#     CTX_LH_PARAHIPPOCAMPAL_SUVR | num     |   284 | DA DECIDERE
#     CTX_LH_PARAHIPPOCAMPAL_VOLUME | num     |   378 | DA DECIDERE
#     CTX_LH_PARSOPERCULARIS_SUVR | num     |   309 | DA DECIDERE
#     CTX_LH_PARSOPERCULARIS_VOLUME | num     |   419 | DA DECIDERE
#     CTX_LH_PARSORBITALIS_SUVR | num     |   347 | DA DECIDERE
#     CTX_LH_PARSORBITALIS_VOLUME | num     |   383 | DA DECIDERE
#     CTX_LH_PARSTRIANGULARIS_SUVR | num     |   332 | DA DECIDERE
#     CTX_LH_PARSTRIANGULARIS_VOLUME | num     |   404 | DA DECIDERE
#     CTX_LH_PERICALCARINE_SUVR | num     |   299 | DA DECIDERE
#     CTX_LH_PERICALCARINE_VOLUME | num     |   400 | DA DECIDERE
#     CTX_LH_POSTCENTRAL_SUVR  | num     |   289 | DA DECIDERE
#     CTX_LH_POSTCENTRAL_VOLUME | num     |   434 | DA DECIDERE
#     CTX_LH_POSTERIORCINGULATE_SUVR | num     |   328 | DA DECIDERE
#     CTX_LH_POSTERIORCINGULATE_VOLUME | num     |   398 | DA DECIDERE
#     CTX_LH_PRECENTRAL_SUVR   | num     |   291 | DA DECIDERE
#     CTX_LH_PRECENTRAL_VOLUME | num     |   446 | DA DECIDERE
#     CTX_LH_PRECUNEUS_SUVR    | num     |   333 | DA DECIDERE
#     CTX_LH_PRECUNEUS_VOLUME  | num     |   441 | DA DECIDERE
#     CTX_LH_ROSTRALANTERIORCINGULATE_SUVR | num     |   345 | DA DECIDERE
#     CTX_LH_ROSTRALANTERIORCINGULATE_VOLUME | num     |   416 | DA DECIDERE
#     CTX_LH_ROSTRALMIDDLEFRONTAL_SUVR | num     |   334 | DA DECIDERE
#     CTX_LH_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   452 | DA DECIDERE
#     CTX_LH_SUPERIORFRONTAL_SUVR | num     |   308 | DA DECIDERE
#     CTX_LH_SUPERIORFRONTAL_VOLUME | num     |   452 | DA DECIDERE
#     CTX_LH_SUPERIORPARIETAL_SUVR | num     |   324 | DA DECIDERE
#     CTX_LH_SUPERIORPARIETAL_VOLUME | num     |   442 | DA DECIDERE
#     CTX_LH_SUPERIORTEMPORAL_SUVR | num     |   312 | DA DECIDERE
#     CTX_LH_SUPERIORTEMPORAL_VOLUME | num     |   442 | DA DECIDERE
#     CTX_LH_SUPRAMARGINAL_SUVR | num     |   320 | DA DECIDERE
#     CTX_LH_SUPRAMARGINAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_LH_TEMPORALPOLE_SUVR | num     |   309 | DA DECIDERE
#     CTX_LH_TEMPORALPOLE_VOLUME | num     |   403 | DA DECIDERE
#     CTX_LH_TRANSVERSETEMPORAL_SUVR | num     |   322 | DA DECIDERE
#     CTX_LH_TRANSVERSETEMPORAL_VOLUME | num     |   345 | DA DECIDERE
#     CTX_RH_BANKSSTS_SUVR     | num     |   341 | DA DECIDERE
#     CTX_RH_BANKSSTS_VOLUME   | num     |   380 | DA DECIDERE
#     CTX_RH_CAUDALANTERIORCINGULATE_SUVR | num     |   348 | DA DECIDERE
#     CTX_RH_CAUDALANTERIORCINGULATE_VOLUME | num     |   394 | DA DECIDERE
#     CTX_RH_CAUDALMIDDLEFRONTAL_SUVR | num     |   334 | DA DECIDERE
#     CTX_RH_CAUDALMIDDLEFRONTAL_VOLUME | num     |   427 | DA DECIDERE
#     CTX_RH_CUNEUS_SUVR       | num     |   297 | DA DECIDERE
#     CTX_RH_CUNEUS_VOLUME     | num     |   412 | DA DECIDERE
#     CTX_RH_ENTORHINAL_SUVR   | num     |   288 | DA DECIDERE
#     CTX_RH_ENTORHINAL_VOLUME | num     |   394 | DA DECIDERE
#     CTX_RH_FRONTALPOLE_SUVR  | num     |   356 | DA DECIDERE
#     CTX_RH_FRONTALPOLE_VOLUME | num     |   341 | DA DECIDERE
#     CTX_RH_FUSIFORM_SUVR     | num     |   294 | DA DECIDERE
#     CTX_RH_FUSIFORM_VOLUME   | num     |   433 | DA DECIDERE
#     CTX_RH_INFERIORPARIETAL_SUVR | num     |   327 | DA DECIDERE
#     CTX_RH_INFERIORPARIETAL_VOLUME | num     |   449 | DA DECIDERE
#     CTX_RH_INFERIORTEMPORAL_SUVR | num     |   326 | DA DECIDERE
#     CTX_RH_INFERIORTEMPORAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_RH_INSULA_SUVR       | num     |   308 | DA DECIDERE
#     CTX_RH_INSULA_VOLUME     | num     |   431 | DA DECIDERE
#     CTX_RH_ISTHMUSCINGULATE_SUVR | num     |   345 | DA DECIDERE
#     CTX_RH_ISTHMUSCINGULATE_VOLUME | num     |   390 | DA DECIDERE
#     CTX_RH_LATERALOCCIPITAL_SUVR | num     |   307 | DA DECIDERE
#     CTX_RH_LATERALOCCIPITAL_VOLUME | num     |   442 | DA DECIDERE
#     CTX_RH_LATERALORBITOFRONTAL_SUVR | num     |   340 | DA DECIDERE
#     CTX_RH_LATERALORBITOFRONTAL_VOLUME | num     |   414 | DA DECIDERE
#     CTX_RH_LINGUAL_SUVR      | num     |   291 | DA DECIDERE
#     CTX_RH_LINGUAL_VOLUME    | num     |   440 | DA DECIDERE
#     CTX_RH_MEDIALORBITOFRONTAL_SUVR | num     |   328 | DA DECIDERE
#     CTX_RH_MEDIALORBITOFRONTAL_VOLUME | num     |   414 | DA DECIDERE
#     CTX_RH_MIDDLETEMPORAL_SUVR | num     |   312 | DA DECIDERE
#     CTX_RH_MIDDLETEMPORAL_VOLUME | num     |   449 | DA DECIDERE
#     CTX_RH_PARACENTRAL_SUVR  | num     |   305 | DA DECIDERE
#     CTX_RH_PARACENTRAL_VOLUME | num     |   400 | DA DECIDERE
#     CTX_RH_PARAHIPPOCAMPAL_SUVR | num     |   295 | DA DECIDERE
#     CTX_RH_PARAHIPPOCAMPAL_VOLUME | num     |   370 | DA DECIDERE
#     CTX_RH_PARSOPERCULARIS_SUVR | num     |   330 | DA DECIDERE
#     CTX_RH_PARSOPERCULARIS_VOLUME | num     |   410 | DA DECIDERE
#     CTX_RH_PARSORBITALIS_SUVR | num     |   344 | DA DECIDERE
#     CTX_RH_PARSORBITALIS_VOLUME | num     |   386 | DA DECIDERE
#     CTX_RH_PARSTRIANGULARIS_SUVR | num     |   331 | DA DECIDERE
#     CTX_RH_PARSTRIANGULARIS_VOLUME | num     |   402 | DA DECIDERE
#     CTX_RH_PERICALCARINE_SUVR | num     |   307 | DA DECIDERE
#     CTX_RH_PERICALCARINE_VOLUME | num     |   396 | DA DECIDERE
#     CTX_RH_POSTCENTRAL_SUVR  | num     |   285 | DA DECIDERE
#     CTX_RH_POSTCENTRAL_VOLUME | num     |   442 | DA DECIDERE
#     CTX_RH_POSTERIORCINGULATE_SUVR | num     |   338 | DA DECIDERE
#     CTX_RH_POSTERIORCINGULATE_VOLUME | num     |   397 | DA DECIDERE
#     CTX_RH_PRECENTRAL_SUVR   | num     |   288 | DA DECIDERE
#     CTX_RH_PRECENTRAL_VOLUME | num     |   445 | DA DECIDERE
#     CTX_RH_PRECUNEUS_SUVR    | num     |   337 | DA DECIDERE
#     CTX_RH_PRECUNEUS_VOLUME  | num     |   437 | DA DECIDERE
#     CTX_RH_ROSTRALANTERIORCINGULATE_SUVR | num     |   356 | DA DECIDERE
#     CTX_RH_ROSTRALANTERIORCINGULATE_VOLUME | num     |   398 | DA DECIDERE
#     CTX_RH_ROSTRALMIDDLEFRONTAL_SUVR | num     |   337 | DA DECIDERE
#     CTX_RH_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   448 | DA DECIDERE
#     CTX_RH_SUPERIORFRONTAL_SUVR | num     |   323 | DA DECIDERE
#     CTX_RH_SUPERIORFRONTAL_VOLUME | num     |   448 | DA DECIDERE
#     CTX_RH_SUPERIORPARIETAL_SUVR | num     |   304 | DA DECIDERE
#     CTX_RH_SUPERIORPARIETAL_VOLUME | num     |   438 | DA DECIDERE
#     CTX_RH_SUPERIORTEMPORAL_SUVR | num     |   299 | DA DECIDERE
#     CTX_RH_SUPERIORTEMPORAL_VOLUME | num     |   444 | DA DECIDERE
#     CTX_RH_SUPRAMARGINAL_SUVR | num     |   322 | DA DECIDERE
#     CTX_RH_SUPRAMARGINAL_VOLUME | num     |   437 | DA DECIDERE
#     CTX_RH_TEMPORALPOLE_SUVR | num     |   310 | DA DECIDERE
#     CTX_RH_TEMPORALPOLE_VOLUME | num     |   393 | DA DECIDERE
#     CTX_RH_TRANSVERSETEMPORAL_SUVR | num     |   307 | DA DECIDERE
#     CTX_RH_TRANSVERSETEMPORAL_VOLUME | num     |   299 | DA DECIDERE
#     LEFT_ACCUMBENS_AREA_SUVR | num     |   340 | DA DECIDERE
#     LEFT_ACCUMBENS_AREA_VOLUME | num     |   285 | DA DECIDERE
#     LEFT_AMYGDALA_SUVR       | num     |   288 | DA DECIDERE
#     LEFT_AMYGDALA_VOLUME     | num     |   374 | DA DECIDERE
#     LEFT_CAUDATE_SUVR        | num     |   305 | DA DECIDERE
#     LEFT_CAUDATE_VOLUME      | num     |   408 | DA DECIDERE
#     LEFT_CEREBELLUM_CORTEX_SUVR | num     |   104 | DA DECIDERE
#     LEFT_CEREBELLUM_CORTEX_VOLUME | num     |   457 | DA DECIDERE
#     LEFT_CEREBELLUM_WHITE_MATTER_SUVR | num     |   270 | DA DECIDERE
#     LEFT_CEREBELLUM_WHITE_MATTER_VOLUME | num     |   445 | DA DECIDERE
#     LEFT_CEREBRAL_WHITE_MATTER_SUVR | num     |   311 | DA DECIDERE
#     LEFT_CEREBRAL_WHITE_MATTER_VOLUME | num     |   461 | DA DECIDERE
#     LEFT_CHOROID_PLEXUS_SUVR | num     |   308 | DA DECIDERE
#     LEFT_CHOROID_PLEXUS_VOLUME | num     |   358 | DA DECIDERE
#     LEFT_HIPPOCAMPUS_SUVR    | num     |   262 | DA DECIDERE
#     LEFT_HIPPOCAMPUS_VOLUME  | num     |   419 | DA DECIDERE
#     LEFT_INF_LAT_VENT_SUVR   | num     |   326 | DA DECIDERE
#     LEFT_INF_LAT_VENT_VOLUME | num     |   389 | DA DECIDERE
#     LEFT_LATERAL_VENTRICLE_SUVR | num     |   330 | DA DECIDERE
#     LEFT_LATERAL_VENTRICLE_VOLUME | num     |   457 | DA DECIDERE
#     LEFT_PALLIDUM_SUVR       | num     |   312 | DA DECIDERE
#     LEFT_PALLIDUM_VOLUME     | num     |   375 | DA DECIDERE
#     LEFT_PUTAMEN_SUVR        | num     |   315 | DA DECIDERE
#     LEFT_PUTAMEN_VOLUME      | num     |   421 | DA DECIDERE
#     LEFT_THALAMUS_PROPER_SUVR | num     |   294 | DA DECIDERE
#     LEFT_THALAMUS_PROPER_VOLUME | num     |   425 | DA DECIDERE
#     LEFT_VENTRALDC_SUVR      | num     |   267 | DA DECIDERE
#     LEFT_VENTRALDC_VOLUME    | num     |   407 | DA DECIDERE
#     LEFT_VESSEL_SUVR         | num     |   320 | DA DECIDERE
#     LEFT_VESSEL_VOLUME       | num     |    90 | DA DECIDERE
#     RIGHT_ACCUMBENS_AREA_SUVR | num     |   364 | DA DECIDERE
#     RIGHT_ACCUMBENS_AREA_VOLUME | num     |   259 | DA DECIDERE
#     RIGHT_AMYGDALA_SUVR      | num     |   276 | DA DECIDERE
#     RIGHT_AMYGDALA_VOLUME    | num     |   375 | DA DECIDERE
#     RIGHT_CAUDATE_SUVR       | num     |   324 | DA DECIDERE
#     RIGHT_CAUDATE_VOLUME     | num     |   404 | DA DECIDERE
#     RIGHT_CEREBELLUM_CORTEX_SUVR | num     |    98 | DA DECIDERE
#     RIGHT_CEREBELLUM_CORTEX_VOLUME | num     |   457 | DA DECIDERE
#     RIGHT_CEREBELLUM_WHITE_MATTER_SUVR | num     |   266 | DA DECIDERE
#     RIGHT_CEREBELLUM_WHITE_MATTER_VOLUME | num     |   448 | DA DECIDERE
#     RIGHT_CEREBRAL_WHITE_MATTER_SUVR | num     |   310 | DA DECIDERE
#     RIGHT_CEREBRAL_WHITE_MATTER_VOLUME | num     |   461 | DA DECIDERE
#     RIGHT_CHOROID_PLEXUS_SUVR | num     |   302 | DA DECIDERE
#     RIGHT_CHOROID_PLEXUS_VOLUME | num     |   359 | DA DECIDERE
#     RIGHT_HIPPOCAMPUS_SUVR   | num     |   259 | DA DECIDERE
#     RIGHT_HIPPOCAMPUS_VOLUME | num     |   423 | DA DECIDERE
#     RIGHT_INF_LAT_VENT_SUVR  | num     |   315 | DA DECIDERE
#     RIGHT_INF_LAT_VENT_VOLUME | num     |   392 | DA DECIDERE
#     RIGHT_LATERAL_VENTRICLE_SUVR | num     |   325 | DA DECIDERE
#     RIGHT_LATERAL_VENTRICLE_VOLUME | num     |   457 | DA DECIDERE
#     RIGHT_PALLIDUM_SUVR      | num     |   303 | DA DECIDERE
#     RIGHT_PALLIDUM_VOLUME    | num     |   363 | DA DECIDERE
#     RIGHT_PUTAMEN_SUVR       | num     |   319 | DA DECIDERE
#     RIGHT_PUTAMEN_VOLUME     | num     |   422 | DA DECIDERE
#     RIGHT_THALAMUS_PROPER_SUVR | num     |   302 | DA DECIDERE
#     RIGHT_THALAMUS_PROPER_VOLUME | num     |   423 | DA DECIDERE
#     RIGHT_VENTRALDC_SUVR     | num     |   264 | DA DECIDERE
#     RIGHT_VENTRALDC_VOLUME   | num     |   404 | DA DECIDERE
#     RIGHT_VESSEL_SUVR        | num     |   326 | DA DECIDERE
#     RIGHT_VESSEL_VOLUME      | num     |    91 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UCBERKELEY_AMY_6MM = DatasetConfig(
    file_code="UCBERKELEY_AMY_6MM",                          # <-- VERIFICA
    source="UCBERKELEY_AMY_6MM_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['pet'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="SCANDATE",          # preferenza ADNI (alt: ['PROCESSDATE', 'update_stamp']) VERIFICA
    # 334 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['IMAGE_RESOLUTION', 'TRACER', 'TRACER_SUVR_WARNING', 'AMYLOID_STATUS', 'AMYLOID_STATUS_COMPOSITE_REF', 'CENTILOIDS', 'SUMMARY_SUVR', 'SUMMARY_VOLUME', 'WHOLECEREBELLUM_SUVR', 'WHOLECEREBELLUM_VOLUME', 'COMPOSITE_REF_SUVR', 'COMPOSITE_REF_VOLUME', 'CEREBELLUM_CORTEX_SUVR', 'CEREBELLUM_CORTEX_VOLUME', 'ERODED_SUBCORTICALWM_SUVR', 'ERODED_SUBCORTICALWM_VOLUME', 'BRAINSTEM_SUVR', 'BRAINSTEM_VOLUME', 'CC_ANTERIOR_SUVR', 'CC_ANTERIOR_VOLUME', 'CC_CENTRAL_SUVR', 'CC_CENTRAL_VOLUME', 'CC_MID_ANTERIOR_SUVR', 'CC_MID_ANTERIOR_VOLUME', 'CC_MID_POSTERIOR_SUVR', 'CC_MID_POSTERIOR_VOLUME', 'CC_POSTERIOR_SUVR', 'CC_POSTERIOR_VOLUME', 'CSF_SUVR', 'CSF_VOLUME', 'VENTRICLE_3RD_SUVR', 'VENTRICLE_3RD_VOLUME', 'VENTRICLE_4TH_SUVR', 'VENTRICLE_4TH_VOLUME', 'VENTRICLE_5TH_SUVR', 'VENTRICLE_5TH_VOLUME', 'WM_HYPOINTENSITIES_SUVR', 'WM_HYPOINTENSITIES_VOLUME', 'NON_WM_HYPOINTENSITIES_SUVR', 'NON_WM_HYPOINTENSITIES_VOLUME', 'CTX_BANKSSTS_SUVR', 'CTX_BANKSSTS_VOLUME', 'CTX_CAUDALANTERIORCINGULATE_SUVR', 'CTX_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_CUNEUS_SUVR', 'CTX_CUNEUS_VOLUME', 'CTX_ENTORHINAL_SUVR', 'CTX_ENTORHINAL_VOLUME', 'CTX_FRONTALPOLE_SUVR', 'CTX_FRONTALPOLE_VOLUME', 'CTX_FUSIFORM_SUVR', 'CTX_FUSIFORM_VOLUME', 'CTX_INFERIORPARIETAL_SUVR', 'CTX_INFERIORPARIETAL_VOLUME', 'CTX_INFERIORTEMPORAL_SUVR', 'CTX_INFERIORTEMPORAL_VOLUME', 'CTX_INSULA_SUVR', 'CTX_INSULA_VOLUME', 'CTX_ISTHMUSCINGULATE_SUVR', 'CTX_ISTHMUSCINGULATE_VOLUME', 'CTX_LATERALOCCIPITAL_SUVR', 'CTX_LATERALOCCIPITAL_VOLUME', 'CTX_LATERALORBITOFRONTAL_SUVR', 'CTX_LATERALORBITOFRONTAL_VOLUME', 'CTX_LINGUAL_SUVR', 'CTX_LINGUAL_VOLUME', 'CTX_MEDIALORBITOFRONTAL_SUVR', 'CTX_MEDIALORBITOFRONTAL_VOLUME', 'CTX_MIDDLETEMPORAL_SUVR', 'CTX_MIDDLETEMPORAL_VOLUME', 'CTX_PARACENTRAL_SUVR', 'CTX_PARACENTRAL_VOLUME', 'CTX_PARAHIPPOCAMPAL_SUVR', 'CTX_PARAHIPPOCAMPAL_VOLUME', 'CTX_PARSOPERCULARIS_SUVR', 'CTX_PARSOPERCULARIS_VOLUME', 'CTX_PARSORBITALIS_SUVR', 'CTX_PARSORBITALIS_VOLUME', 'CTX_PARSTRIANGULARIS_SUVR', 'CTX_PARSTRIANGULARIS_VOLUME', 'CTX_PERICALCARINE_SUVR', 'CTX_PERICALCARINE_VOLUME', 'CTX_POSTCENTRAL_SUVR', 'CTX_POSTCENTRAL_VOLUME', 'CTX_POSTERIORCINGULATE_SUVR', 'CTX_POSTERIORCINGULATE_VOLUME', 'CTX_PRECENTRAL_SUVR', 'CTX_PRECENTRAL_VOLUME', 'CTX_PRECUNEUS_SUVR', 'CTX_PRECUNEUS_VOLUME', 'CTX_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_SUPERIORFRONTAL_SUVR', 'CTX_SUPERIORFRONTAL_VOLUME', 'CTX_SUPERIORPARIETAL_SUVR', 'CTX_SUPERIORPARIETAL_VOLUME', 'CTX_SUPERIORTEMPORAL_SUVR', 'CTX_SUPERIORTEMPORAL_VOLUME', 'CTX_SUPRAMARGINAL_SUVR', 'CTX_SUPRAMARGINAL_VOLUME', 'CTX_TEMPORALPOLE_SUVR', 'CTX_TEMPORALPOLE_VOLUME', 'CTX_TRANSVERSETEMPORAL_SUVR', 'CTX_TRANSVERSETEMPORAL_VOLUME', 'ACCUMBENS_AREA_SUVR', 'ACCUMBENS_AREA_VOLUME', 'AMYGDALA_SUVR', 'AMYGDALA_VOLUME', 'CAUDATE_SUVR', 'CAUDATE_VOLUME', 'CEREBELLUM_WHITE_MATTER_SUVR', 'CEREBELLUM_WHITE_MATTER_VOLUME', 'CEREBRAL_WHITE_MATTER_SUVR', 'CEREBRAL_WHITE_MATTER_VOLUME', 'CHOROID_PLEXUS_SUVR', 'CHOROID_PLEXUS_VOLUME', 'HIPPOCAMPUS_SUVR', 'HIPPOCAMPUS_VOLUME', 'OPTIC_CHIASM_SUVR', 'OPTIC_CHIASM_VOLUME', 'INF_LAT_VENT_SUVR', 'INF_LAT_VENT_VOLUME', 'LATERAL_VENTRICLE_SUVR', 'LATERAL_VENTRICLE_VOLUME', 'PALLIDUM_SUVR', 'PALLIDUM_VOLUME', 'PUTAMEN_SUVR', 'PUTAMEN_VOLUME', 'THALAMUS_PROPER_SUVR', 'THALAMUS_PROPER_VOLUME', 'VENTRALDC_SUVR', 'VENTRALDC_VOLUME', 'VESSEL_SUVR', 'VESSEL_VOLUME', 'CTX_LH_BANKSSTS_SUVR', 'CTX_LH_BANKSSTS_VOLUME', 'CTX_LH_CAUDALANTERIORCINGULATE_SUVR', 'CTX_LH_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_LH_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_LH_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_LH_CUNEUS_SUVR', 'CTX_LH_CUNEUS_VOLUME', 'CTX_LH_ENTORHINAL_SUVR', 'CTX_LH_ENTORHINAL_VOLUME', 'CTX_LH_FRONTALPOLE_SUVR', 'CTX_LH_FRONTALPOLE_VOLUME', 'CTX_LH_FUSIFORM_SUVR', 'CTX_LH_FUSIFORM_VOLUME', 'CTX_LH_INFERIORPARIETAL_SUVR', 'CTX_LH_INFERIORPARIETAL_VOLUME', 'CTX_LH_INFERIORTEMPORAL_SUVR', 'CTX_LH_INFERIORTEMPORAL_VOLUME', 'CTX_LH_INSULA_SUVR', 'CTX_LH_INSULA_VOLUME', 'CTX_LH_ISTHMUSCINGULATE_SUVR', 'CTX_LH_ISTHMUSCINGULATE_VOLUME', 'CTX_LH_LATERALOCCIPITAL_SUVR', 'CTX_LH_LATERALOCCIPITAL_VOLUME', 'CTX_LH_LATERALORBITOFRONTAL_SUVR', 'CTX_LH_LATERALORBITOFRONTAL_VOLUME', 'CTX_LH_LINGUAL_SUVR', 'CTX_LH_LINGUAL_VOLUME', 'CTX_LH_MEDIALORBITOFRONTAL_SUVR', 'CTX_LH_MEDIALORBITOFRONTAL_VOLUME', 'CTX_LH_MIDDLETEMPORAL_SUVR', 'CTX_LH_MIDDLETEMPORAL_VOLUME', 'CTX_LH_PARACENTRAL_SUVR', 'CTX_LH_PARACENTRAL_VOLUME', 'CTX_LH_PARAHIPPOCAMPAL_SUVR', 'CTX_LH_PARAHIPPOCAMPAL_VOLUME', 'CTX_LH_PARSOPERCULARIS_SUVR', 'CTX_LH_PARSOPERCULARIS_VOLUME', 'CTX_LH_PARSORBITALIS_SUVR', 'CTX_LH_PARSORBITALIS_VOLUME', 'CTX_LH_PARSTRIANGULARIS_SUVR', 'CTX_LH_PARSTRIANGULARIS_VOLUME', 'CTX_LH_PERICALCARINE_SUVR', 'CTX_LH_PERICALCARINE_VOLUME', 'CTX_LH_POSTCENTRAL_SUVR', 'CTX_LH_POSTCENTRAL_VOLUME', 'CTX_LH_POSTERIORCINGULATE_SUVR', 'CTX_LH_POSTERIORCINGULATE_VOLUME', 'CTX_LH_PRECENTRAL_SUVR', 'CTX_LH_PRECENTRAL_VOLUME', 'CTX_LH_PRECUNEUS_SUVR', 'CTX_LH_PRECUNEUS_VOLUME', 'CTX_LH_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_LH_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_LH_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_LH_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_LH_SUPERIORFRONTAL_SUVR', 'CTX_LH_SUPERIORFRONTAL_VOLUME', 'CTX_LH_SUPERIORPARIETAL_SUVR', 'CTX_LH_SUPERIORPARIETAL_VOLUME', 'CTX_LH_SUPERIORTEMPORAL_SUVR', 'CTX_LH_SUPERIORTEMPORAL_VOLUME', 'CTX_LH_SUPRAMARGINAL_SUVR', 'CTX_LH_SUPRAMARGINAL_VOLUME', 'CTX_LH_TEMPORALPOLE_SUVR', 'CTX_LH_TEMPORALPOLE_VOLUME', 'CTX_LH_TRANSVERSETEMPORAL_SUVR', 'CTX_LH_TRANSVERSETEMPORAL_VOLUME', 'CTX_RH_BANKSSTS_SUVR', 'CTX_RH_BANKSSTS_VOLUME', 'CTX_RH_CAUDALANTERIORCINGULATE_SUVR', 'CTX_RH_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_RH_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_RH_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_RH_CUNEUS_SUVR', 'CTX_RH_CUNEUS_VOLUME', 'CTX_RH_ENTORHINAL_SUVR', 'CTX_RH_ENTORHINAL_VOLUME', 'CTX_RH_FRONTALPOLE_SUVR', 'CTX_RH_FRONTALPOLE_VOLUME', 'CTX_RH_FUSIFORM_SUVR', 'CTX_RH_FUSIFORM_VOLUME', 'CTX_RH_INFERIORPARIETAL_SUVR', 'CTX_RH_INFERIORPARIETAL_VOLUME', 'CTX_RH_INFERIORTEMPORAL_SUVR', 'CTX_RH_INFERIORTEMPORAL_VOLUME', 'CTX_RH_INSULA_SUVR', 'CTX_RH_INSULA_VOLUME', 'CTX_RH_ISTHMUSCINGULATE_SUVR', 'CTX_RH_ISTHMUSCINGULATE_VOLUME', 'CTX_RH_LATERALOCCIPITAL_SUVR', 'CTX_RH_LATERALOCCIPITAL_VOLUME', 'CTX_RH_LATERALORBITOFRONTAL_SUVR', 'CTX_RH_LATERALORBITOFRONTAL_VOLUME', 'CTX_RH_LINGUAL_SUVR', 'CTX_RH_LINGUAL_VOLUME', 'CTX_RH_MEDIALORBITOFRONTAL_SUVR', 'CTX_RH_MEDIALORBITOFRONTAL_VOLUME', 'CTX_RH_MIDDLETEMPORAL_SUVR', 'CTX_RH_MIDDLETEMPORAL_VOLUME', 'CTX_RH_PARACENTRAL_SUVR', 'CTX_RH_PARACENTRAL_VOLUME', 'CTX_RH_PARAHIPPOCAMPAL_SUVR', 'CTX_RH_PARAHIPPOCAMPAL_VOLUME', 'CTX_RH_PARSOPERCULARIS_SUVR', 'CTX_RH_PARSOPERCULARIS_VOLUME', 'CTX_RH_PARSORBITALIS_SUVR', 'CTX_RH_PARSORBITALIS_VOLUME', 'CTX_RH_PARSTRIANGULARIS_SUVR', 'CTX_RH_PARSTRIANGULARIS_VOLUME', 'CTX_RH_PERICALCARINE_SUVR', 'CTX_RH_PERICALCARINE_VOLUME', 'CTX_RH_POSTCENTRAL_SUVR', 'CTX_RH_POSTCENTRAL_VOLUME', 'CTX_RH_POSTERIORCINGULATE_SUVR', 'CTX_RH_POSTERIORCINGULATE_VOLUME', 'CTX_RH_PRECENTRAL_SUVR', 'CTX_RH_PRECENTRAL_VOLUME', 'CTX_RH_PRECUNEUS_SUVR', 'CTX_RH_PRECUNEUS_VOLUME', 'CTX_RH_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_RH_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_RH_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_RH_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_RH_SUPERIORFRONTAL_SUVR', 'CTX_RH_SUPERIORFRONTAL_VOLUME', 'CTX_RH_SUPERIORPARIETAL_SUVR', 'CTX_RH_SUPERIORPARIETAL_VOLUME', 'CTX_RH_SUPERIORTEMPORAL_SUVR', 'CTX_RH_SUPERIORTEMPORAL_VOLUME', 'CTX_RH_SUPRAMARGINAL_SUVR', 'CTX_RH_SUPRAMARGINAL_VOLUME', 'CTX_RH_TEMPORALPOLE_SUVR', 'CTX_RH_TEMPORALPOLE_VOLUME', 'CTX_RH_TRANSVERSETEMPORAL_SUVR', 'CTX_RH_TRANSVERSETEMPORAL_VOLUME', 'LEFT_ACCUMBENS_AREA_SUVR', 'LEFT_ACCUMBENS_AREA_VOLUME', 'LEFT_AMYGDALA_SUVR', 'LEFT_AMYGDALA_VOLUME', 'LEFT_CAUDATE_SUVR', 'LEFT_CAUDATE_VOLUME', 'LEFT_CEREBELLUM_CORTEX_SUVR', 'LEFT_CEREBELLUM_CORTEX_VOLUME', 'LEFT_CEREBELLUM_WHITE_MATTER_SUVR', 'LEFT_CEREBELLUM_WHITE_MATTER_VOLUME', 'LEFT_CEREBRAL_WHITE_MATTER_SUVR', 'LEFT_CEREBRAL_WHITE_MATTER_VOLUME', 'LEFT_CHOROID_PLEXUS_SUVR', 'LEFT_CHOROID_PLEXUS_VOLUME', 'LEFT_HIPPOCAMPUS_SUVR', 'LEFT_HIPPOCAMPUS_VOLUME', 'LEFT_INF_LAT_VENT_SUVR', 'LEFT_INF_LAT_VENT_VOLUME', 'LEFT_LATERAL_VENTRICLE_SUVR', 'LEFT_LATERAL_VENTRICLE_VOLUME', 'LEFT_PALLIDUM_SUVR', 'LEFT_PALLIDUM_VOLUME', 'LEFT_PUTAMEN_SUVR', 'LEFT_PUTAMEN_VOLUME', 'LEFT_THALAMUS_PROPER_SUVR', 'LEFT_THALAMUS_PROPER_VOLUME', 'LEFT_VENTRALDC_SUVR', 'LEFT_VENTRALDC_VOLUME', 'LEFT_VESSEL_SUVR', 'LEFT_VESSEL_VOLUME', 'RIGHT_ACCUMBENS_AREA_SUVR', 'RIGHT_ACCUMBENS_AREA_VOLUME', 'RIGHT_AMYGDALA_SUVR', 'RIGHT_AMYGDALA_VOLUME', 'RIGHT_CAUDATE_SUVR', 'RIGHT_CAUDATE_VOLUME', 'RIGHT_CEREBELLUM_CORTEX_SUVR', 'RIGHT_CEREBELLUM_CORTEX_VOLUME', 'RIGHT_CEREBELLUM_WHITE_MATTER_SUVR', 'RIGHT_CEREBELLUM_WHITE_MATTER_VOLUME', 'RIGHT_CEREBRAL_WHITE_MATTER_SUVR', 'RIGHT_CEREBRAL_WHITE_MATTER_VOLUME', 'RIGHT_CHOROID_PLEXUS_SUVR', 'RIGHT_CHOROID_PLEXUS_VOLUME', 'RIGHT_HIPPOCAMPUS_SUVR', 'RIGHT_HIPPOCAMPUS_VOLUME', 'RIGHT_INF_LAT_VENT_SUVR', 'RIGHT_INF_LAT_VENT_VOLUME', 'RIGHT_LATERAL_VENTRICLE_SUVR', 'RIGHT_LATERAL_VENTRICLE_VOLUME', 'RIGHT_PALLIDUM_SUVR', 'RIGHT_PALLIDUM_VOLUME', 'RIGHT_PUTAMEN_SUVR', 'RIGHT_PUTAMEN_VOLUME', 'RIGHT_THALAMUS_PROPER_SUVR', 'RIGHT_THALAMUS_PROPER_VOLUME', 'RIGHT_VENTRALDC_SUVR', 'RIGHT_VENTRALDC_VOLUME', 'RIGHT_VESSEL_SUVR', 'RIGHT_VESSEL_VOLUME']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCBERKELEY_TAUPVC_6MM
#   source: UCBERKELEY_TAUPVC_6MM_28Oct2025.csv   |   righe campionate: 500   |   colonne: 335
#   INDIZIO categoria dal nome (NON deciso): ['pet']
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   262 | cand. ID
#     RID                      | num     |   262 | cand. ID
#     VISCODE                  | cat/str |     9 | cand. VISITA
#     VISCODE2                 | cat/str |    27 | cand. VISITA
#     SCANDATE                 | date    |   387 | cand. DATA
#     PROCESSDATE              | date    |    30 | cand. DATA
#     TRACER                   | cat/str |     1 | DA DECIDERE
#     TRACER_SUVR_WARNING      | cat/str |     1 | DA DECIDERE
#     META_TEMPORAL_SUVR       | num     |   356 | DA DECIDERE
#     META_TEMPORAL_VOLUME     | num     |   457 | DA DECIDERE
#     CTX_ENTORHINAL_SUVR      | num     |   396 | DA DECIDERE
#     CTX_ENTORHINAL_VOLUME    | num     |   424 | DA DECIDERE
#     INFERIORCEREBELLUM_SUVR  | num     |     1 | DA DECIDERE
#     INFERIORCEREBELLUM_VOLUME | num     |   461 | DA DECIDERE
#     CEREBRAL_WHITE_MATTER_SUVR | num     |   327 | DA DECIDERE
#     CEREBRAL_WHITE_MATTER_VOLUME | num     |   462 | DA DECIDERE
#     BRAINSTEM_SUVR           | num     |   291 | DA DECIDERE
#     BRAINSTEM_VOLUME         | num     |   452 | DA DECIDERE
#     CC_ANTERIOR_SUVR         | num     |   328 | DA DECIDERE
#     CC_ANTERIOR_VOLUME       | num     |   323 | DA DECIDERE
#     CC_CENTRAL_SUVR          | num     |   328 | DA DECIDERE
#     CC_CENTRAL_VOLUME        | num     |   256 | DA DECIDERE
#     CC_MID_ANTERIOR_SUVR     | num     |   328 | DA DECIDERE
#     CC_MID_ANTERIOR_VOLUME   | num     |   257 | DA DECIDERE
#     CC_MID_POSTERIOR_SUVR    | num     |   329 | DA DECIDERE
#     CC_MID_POSTERIOR_VOLUME  | num     |   289 | DA DECIDERE
#     CC_POSTERIOR_SUVR        | num     |   328 | DA DECIDERE
#     CC_POSTERIOR_VOLUME      | num     |   307 | DA DECIDERE
#     CSF_SUVR                 | num     |   277 | DA DECIDERE
#     CSF_VOLUME               | num     |   382 | DA DECIDERE
#     VENTRICLE_3RD_SUVR       | num     |   285 | DA DECIDERE
#     VENTRICLE_3RD_VOLUME     | num     |   415 | DA DECIDERE
#     VENTRICLE_4TH_SUVR       | num     |   289 | DA DECIDERE
#     VENTRICLE_4TH_VOLUME     | num     |   416 | DA DECIDERE
#     VENTRICLE_5TH_SUVR       | num     |     6 | DA DECIDERE
#     VENTRICLE_5TH_VOLUME     | num     |     6 | DA DECIDERE
#     WM_HYPOINTENSITIES_SUVR  | num     |   302 | DA DECIDERE
#     WM_HYPOINTENSITIES_VOLUME | num     |   450 | DA DECIDERE
#     NON_WM_HYPOINTENSITIES_SUVR | num     |    40 | DA DECIDERE
#     NON_WM_HYPOINTENSITIES_VOLUME | num     |     9 | DA DECIDERE
#     CTX_BANKSSTS_SUVR        | num     |   358 | DA DECIDERE
#     CTX_BANKSSTS_VOLUME      | num     |   423 | DA DECIDERE
#     CTX_CAUDALANTERIORCINGULATE_SUVR | num     |   323 | DA DECIDERE
#     CTX_CAUDALANTERIORCINGULATE_VOLUME | num     |   410 | DA DECIDERE
#     CTX_CAUDALMIDDLEFRONTAL_SUVR | num     |   335 | DA DECIDERE
#     CTX_CAUDALMIDDLEFRONTAL_VOLUME | num     |   448 | DA DECIDERE
#     CTX_CUNEUS_SUVR          | num     |   320 | DA DECIDERE
#     CTX_CUNEUS_VOLUME        | num     |   433 | DA DECIDERE
#     CTX_FRONTALPOLE_SUVR     | num     |   370 | DA DECIDERE
#     CTX_FRONTALPOLE_VOLUME   | num     |   392 | DA DECIDERE
#     CTX_FUSIFORM_SUVR        | num     |   337 | DA DECIDERE
#     CTX_FUSIFORM_VOLUME      | num     |   449 | DA DECIDERE
#     CTX_INFERIORPARIETAL_SUVR | num     |   336 | DA DECIDERE
#     CTX_INFERIORPARIETAL_VOLUME | num     |   455 | DA DECIDERE
#     CTX_INFERIORTEMPORAL_SUVR | num     |   362 | DA DECIDERE
#     CTX_INFERIORTEMPORAL_VOLUME | num     |   456 | DA DECIDERE
#     CTX_INSULA_SUVR          | num     |   315 | DA DECIDERE
#     CTX_INSULA_VOLUME        | num     |   436 | DA DECIDERE
#     CTX_ISTHMUSCINGULATE_SUVR | num     |   344 | DA DECIDERE
#     CTX_ISTHMUSCINGULATE_VOLUME | num     |   422 | DA DECIDERE
#     CTX_LATERALOCCIPITAL_SUVR | num     |   356 | DA DECIDERE
#     CTX_LATERALOCCIPITAL_VOLUME | num     |   455 | DA DECIDERE
#     CTX_LATERALORBITOFRONTAL_SUVR | num     |   321 | DA DECIDERE
#     CTX_LATERALORBITOFRONTAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_LINGUAL_SUVR         | num     |   333 | DA DECIDERE
#     CTX_LINGUAL_VOLUME       | num     |   447 | DA DECIDERE
#     CTX_MEDIALORBITOFRONTAL_SUVR | num     |   324 | DA DECIDERE
#     CTX_MEDIALORBITOFRONTAL_VOLUME | num     |   437 | DA DECIDERE
#     CTX_MIDDLETEMPORAL_SUVR  | num     |   357 | DA DECIDERE
#     CTX_MIDDLETEMPORAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_PARACENTRAL_SUVR     | num     |   300 | DA DECIDERE
#     CTX_PARACENTRAL_VOLUME   | num     |   423 | DA DECIDERE
#     CTX_PARAHIPPOCAMPAL_SUVR | num     |   360 | DA DECIDERE
#     CTX_PARAHIPPOCAMPAL_VOLUME | num     |   399 | DA DECIDERE
#     CTX_PARSOPERCULARIS_SUVR | num     |   322 | DA DECIDERE
#     CTX_PARSOPERCULARIS_VOLUME | num     |   438 | DA DECIDERE
#     CTX_PARSORBITALIS_SUVR   | num     |   331 | DA DECIDERE
#     CTX_PARSORBITALIS_VOLUME | num     |   401 | DA DECIDERE
#     CTX_PARSTRIANGULARIS_SUVR | num     |   323 | DA DECIDERE
#     CTX_PARSTRIANGULARIS_VOLUME | num     |   430 | DA DECIDERE
#     CTX_PERICALCARINE_SUVR   | num     |   337 | DA DECIDERE
#     CTX_PERICALCARINE_VOLUME | num     |   436 | DA DECIDERE
#     CTX_POSTCENTRAL_SUVR     | num     |   299 | DA DECIDERE
#     CTX_POSTCENTRAL_VOLUME   | num     |   456 | DA DECIDERE
#     CTX_POSTERIORCINGULATE_SUVR | num     |   335 | DA DECIDERE
#     CTX_POSTERIORCINGULATE_VOLUME | num     |   416 | DA DECIDERE
#     CTX_PRECENTRAL_SUVR      | num     |   277 | DA DECIDERE
#     CTX_PRECENTRAL_VOLUME    | num     |   452 | DA DECIDERE
#     CTX_PRECUNEUS_SUVR       | num     |   333 | DA DECIDERE
#     CTX_PRECUNEUS_VOLUME     | num     |   439 | DA DECIDERE
#     CTX_ROSTRALANTERIORCINGULATE_SUVR | num     |   307 | DA DECIDERE
#     CTX_ROSTRALANTERIORCINGULATE_VOLUME | num     |   425 | DA DECIDERE
#     CTX_ROSTRALMIDDLEFRONTAL_SUVR | num     |   333 | DA DECIDERE
#     CTX_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   453 | DA DECIDERE
#     CTX_SUPERIORFRONTAL_SUVR | num     |   314 | DA DECIDERE
#     CTX_SUPERIORFRONTAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_SUPERIORPARIETAL_SUVR | num     |   333 | DA DECIDERE
#     CTX_SUPERIORPARIETAL_VOLUME | num     |   454 | DA DECIDERE
#     CTX_SUPERIORTEMPORAL_SUVR | num     |   334 | DA DECIDERE
#     CTX_SUPERIORTEMPORAL_VOLUME | num     |   445 | DA DECIDERE
#     CTX_SUPRAMARGINAL_SUVR   | num     |   319 | DA DECIDERE
#     CTX_SUPRAMARGINAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_TEMPORALPOLE_SUVR    | num     |   355 | DA DECIDERE
#     CTX_TEMPORALPOLE_VOLUME  | num     |   435 | DA DECIDERE
#     CTX_TRANSVERSETEMPORAL_SUVR | num     |   330 | DA DECIDERE
#     CTX_TRANSVERSETEMPORAL_VOLUME | num     |   379 | DA DECIDERE
#     ACCUMBENS_AREA_SUVR      | num     |   399 | DA DECIDERE
#     ACCUMBENS_AREA_VOLUME    | num     |   325 | DA DECIDERE
#     AMYGDALA_SUVR            | num     |   376 | DA DECIDERE
#     AMYGDALA_VOLUME          | num     |   405 | DA DECIDERE
#     CAUDATE_SUVR             | num     |   375 | DA DECIDERE
#     CAUDATE_VOLUME           | num     |   430 | DA DECIDERE
#     CEREBELLUM_CORTEX_SUVR   | num     |   125 | DA DECIDERE
#     CEREBELLUM_CORTEX_VOLUME | num     |   461 | DA DECIDERE
#     CEREBELLUM_WHITE_MATTER_SUVR | num     |   298 | DA DECIDERE
#     CEREBELLUM_WHITE_MATTER_VOLUME | num     |   454 | DA DECIDERE
#     CHOROID_PLEXUS_SUVR      | num     |   472 | DA DECIDERE
#     CHOROID_PLEXUS_VOLUME    | num     |   400 | DA DECIDERE
#     HIPPOCAMPUS_SUVR         | num     |   345 | DA DECIDERE
#     HIPPOCAMPUS_VOLUME       | num     |   426 | DA DECIDERE
#     OPTIC_CHIASM_SUVR        | num     |   417 | DA DECIDERE
#     OPTIC_CHIASM_VOLUME      | num     |   151 | DA DECIDERE
#     INF_LAT_VENT_SUVR        | num     |   429 | DA DECIDERE
#     INF_LAT_VENT_VOLUME      | num     |   425 | DA DECIDERE
#     LATERAL_VENTRICLE_SUVR   | num     |   257 | DA DECIDERE
#     LATERAL_VENTRICLE_VOLUME | num     |   460 | DA DECIDERE
#     PALLIDUM_SUVR            | num     |   401 | DA DECIDERE
#     PALLIDUM_VOLUME          | num     |   404 | DA DECIDERE
#     PUTAMEN_SUVR             | num     |   377 | DA DECIDERE
#     PUTAMEN_VOLUME           | num     |   429 | DA DECIDERE
#     THALAMUS_PROPER_SUVR     | num     |   300 | DA DECIDERE
#     THALAMUS_PROPER_VOLUME   | num     |   444 | DA DECIDERE
#     VENTRALDC_SUVR           | num     |   333 | DA DECIDERE
#     VENTRALDC_VOLUME         | num     |   420 | DA DECIDERE
#     VESSEL_SUVR              | vuota   |     0 | DA DECIDERE
#     VESSEL_VOLUME            | num     |   137 | DA DECIDERE
#     CTX_LH_BANKSSTS_SUVR     | num     |   378 | DA DECIDERE
#     CTX_LH_BANKSSTS_VOLUME   | num     |   392 | DA DECIDERE
#     CTX_LH_CAUDALANTERIORCINGULATE_SUVR | num     |   316 | DA DECIDERE
#     CTX_LH_CAUDALANTERIORCINGULATE_VOLUME | num     |   394 | DA DECIDERE
#     CTX_LH_CAUDALMIDDLEFRONTAL_SUVR | num     |   328 | DA DECIDERE
#     CTX_LH_CAUDALMIDDLEFRONTAL_VOLUME | num     |   435 | DA DECIDERE
#     CTX_LH_CUNEUS_SUVR       | num     |   348 | DA DECIDERE
#     CTX_LH_CUNEUS_VOLUME     | num     |   408 | DA DECIDERE
#     CTX_LH_ENTORHINAL_SUVR   | num     |   393 | DA DECIDERE
#     CTX_LH_ENTORHINAL_VOLUME | num     |   398 | DA DECIDERE
#     CTX_LH_FRONTALPOLE_SUVR  | num     |   366 | DA DECIDERE
#     CTX_LH_FRONTALPOLE_VOLUME | num     |   342 | DA DECIDERE
#     CTX_LH_FUSIFORM_SUVR     | num     |   358 | DA DECIDERE
#     CTX_LH_FUSIFORM_VOLUME   | num     |   437 | DA DECIDERE
#     CTX_LH_INFERIORPARIETAL_SUVR | num     |   350 | DA DECIDERE
#     CTX_LH_INFERIORPARIETAL_VOLUME | num     |   446 | DA DECIDERE
#     CTX_LH_INFERIORTEMPORAL_SUVR | num     |   352 | DA DECIDERE
#     CTX_LH_INFERIORTEMPORAL_VOLUME | num     |   447 | DA DECIDERE
#     CTX_LH_INSULA_SUVR       | num     |   313 | DA DECIDERE
#     CTX_LH_INSULA_VOLUME     | num     |   422 | DA DECIDERE
#     CTX_LH_ISTHMUSCINGULATE_SUVR | num     |   355 | DA DECIDERE
#     CTX_LH_ISTHMUSCINGULATE_VOLUME | num     |   397 | DA DECIDERE
#     CTX_LH_LATERALOCCIPITAL_SUVR | num     |   372 | DA DECIDERE
#     CTX_LH_LATERALOCCIPITAL_VOLUME | num     |   445 | DA DECIDERE
#     CTX_LH_LATERALORBITOFRONTAL_SUVR | num     |   335 | DA DECIDERE
#     CTX_LH_LATERALORBITOFRONTAL_VOLUME | num     |   416 | DA DECIDERE
#     CTX_LH_LINGUAL_SUVR      | num     |   321 | DA DECIDERE
#     CTX_LH_LINGUAL_VOLUME    | num     |   431 | DA DECIDERE
#     CTX_LH_MEDIALORBITOFRONTAL_SUVR | num     |   327 | DA DECIDERE
#     CTX_LH_MEDIALORBITOFRONTAL_VOLUME | num     |   420 | DA DECIDERE
#     CTX_LH_MIDDLETEMPORAL_SUVR | num     |   347 | DA DECIDERE
#     CTX_LH_MIDDLETEMPORAL_VOLUME | num     |   437 | DA DECIDERE
#     CTX_LH_PARACENTRAL_SUVR  | num     |   298 | DA DECIDERE
#     CTX_LH_PARACENTRAL_VOLUME | num     |   392 | DA DECIDERE
#     CTX_LH_PARAHIPPOCAMPAL_SUVR | num     |   371 | DA DECIDERE
#     CTX_LH_PARAHIPPOCAMPAL_VOLUME | num     |   368 | DA DECIDERE
#     CTX_LH_PARSOPERCULARIS_SUVR | num     |   315 | DA DECIDERE
#     CTX_LH_PARSOPERCULARIS_VOLUME | num     |   418 | DA DECIDERE
#     CTX_LH_PARSORBITALIS_SUVR | num     |   329 | DA DECIDERE
#     CTX_LH_PARSORBITALIS_VOLUME | num     |   383 | DA DECIDERE
#     CTX_LH_PARSTRIANGULARIS_SUVR | num     |   323 | DA DECIDERE
#     CTX_LH_PARSTRIANGULARIS_VOLUME | num     |   409 | DA DECIDERE
#     CTX_LH_PERICALCARINE_SUVR | num     |   342 | DA DECIDERE
#     CTX_LH_PERICALCARINE_VOLUME | num     |   396 | DA DECIDERE
#     CTX_LH_POSTCENTRAL_SUVR  | num     |   304 | DA DECIDERE
#     CTX_LH_POSTCENTRAL_VOLUME | num     |   441 | DA DECIDERE
#     CTX_LH_POSTERIORCINGULATE_SUVR | num     |   338 | DA DECIDERE
#     CTX_LH_POSTERIORCINGULATE_VOLUME | num     |   395 | DA DECIDERE
#     CTX_LH_PRECENTRAL_SUVR   | num     |   286 | DA DECIDERE
#     CTX_LH_PRECENTRAL_VOLUME | num     |   441 | DA DECIDERE
#     CTX_LH_PRECUNEUS_SUVR    | num     |   322 | DA DECIDERE
#     CTX_LH_PRECUNEUS_VOLUME  | num     |   440 | DA DECIDERE
#     CTX_LH_ROSTRALANTERIORCINGULATE_SUVR | num     |   307 | DA DECIDERE
#     CTX_LH_ROSTRALANTERIORCINGULATE_VOLUME | num     |   402 | DA DECIDERE
#     CTX_LH_ROSTRALMIDDLEFRONTAL_SUVR | num     |   318 | DA DECIDERE
#     CTX_LH_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   450 | DA DECIDERE
#     CTX_LH_SUPERIORFRONTAL_SUVR | num     |   330 | DA DECIDERE
#     CTX_LH_SUPERIORFRONTAL_VOLUME | num     |   452 | DA DECIDERE
#     CTX_LH_SUPERIORPARIETAL_SUVR | num     |   335 | DA DECIDERE
#     CTX_LH_SUPERIORPARIETAL_VOLUME | num     |   438 | DA DECIDERE
#     CTX_LH_SUPERIORTEMPORAL_SUVR | num     |   319 | DA DECIDERE
#     CTX_LH_SUPERIORTEMPORAL_VOLUME | num     |   444 | DA DECIDERE
#     CTX_LH_SUPRAMARGINAL_SUVR | num     |   326 | DA DECIDERE
#     CTX_LH_SUPRAMARGINAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_LH_TEMPORALPOLE_SUVR | num     |   363 | DA DECIDERE
#     CTX_LH_TEMPORALPOLE_VOLUME | num     |   413 | DA DECIDERE
#     CTX_LH_TRANSVERSETEMPORAL_SUVR | num     |   338 | DA DECIDERE
#     CTX_LH_TRANSVERSETEMPORAL_VOLUME | num     |   336 | DA DECIDERE
#     CTX_RH_BANKSSTS_SUVR     | num     |   375 | DA DECIDERE
#     CTX_RH_BANKSSTS_VOLUME   | num     |   366 | DA DECIDERE
#     CTX_RH_CAUDALANTERIORCINGULATE_SUVR | num     |   321 | DA DECIDERE
#     CTX_RH_CAUDALANTERIORCINGULATE_VOLUME | num     |   389 | DA DECIDERE
#     CTX_RH_CAUDALMIDDLEFRONTAL_SUVR | num     |   344 | DA DECIDERE
#     CTX_RH_CAUDALMIDDLEFRONTAL_VOLUME | num     |   425 | DA DECIDERE
#     CTX_RH_CUNEUS_SUVR       | num     |   321 | DA DECIDERE
#     CTX_RH_CUNEUS_VOLUME     | num     |   424 | DA DECIDERE
#     CTX_RH_ENTORHINAL_SUVR   | num     |   407 | DA DECIDERE
#     CTX_RH_ENTORHINAL_VOLUME | num     |   396 | DA DECIDERE
#     CTX_RH_FRONTALPOLE_SUVR  | num     |   355 | DA DECIDERE
#     CTX_RH_FRONTALPOLE_VOLUME | num     |   343 | DA DECIDERE
#     CTX_RH_FUSIFORM_SUVR     | num     |   353 | DA DECIDERE
#     CTX_RH_FUSIFORM_VOLUME   | num     |   430 | DA DECIDERE
#     CTX_RH_INFERIORPARIETAL_SUVR | num     |   351 | DA DECIDERE
#     CTX_RH_INFERIORPARIETAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_RH_INFERIORTEMPORAL_SUVR | num     |   350 | DA DECIDERE
#     CTX_RH_INFERIORTEMPORAL_VOLUME | num     |   435 | DA DECIDERE
#     CTX_RH_INSULA_SUVR       | num     |   313 | DA DECIDERE
#     CTX_RH_INSULA_VOLUME     | num     |   423 | DA DECIDERE
#     CTX_RH_ISTHMUSCINGULATE_SUVR | num     |   344 | DA DECIDERE
#     CTX_RH_ISTHMUSCINGULATE_VOLUME | num     |   382 | DA DECIDERE
#     CTX_RH_LATERALOCCIPITAL_SUVR | num     |   362 | DA DECIDERE
#     CTX_RH_LATERALOCCIPITAL_VOLUME | num     |   444 | DA DECIDERE
#     CTX_RH_LATERALORBITOFRONTAL_SUVR | num     |   330 | DA DECIDERE
#     CTX_RH_LATERALORBITOFRONTAL_VOLUME | num     |   412 | DA DECIDERE
#     CTX_RH_LINGUAL_SUVR      | num     |   318 | DA DECIDERE
#     CTX_RH_LINGUAL_VOLUME    | num     |   436 | DA DECIDERE
#     CTX_RH_MEDIALORBITOFRONTAL_SUVR | num     |   334 | DA DECIDERE
#     CTX_RH_MEDIALORBITOFRONTAL_VOLUME | num     |   419 | DA DECIDERE
#     CTX_RH_MIDDLETEMPORAL_SUVR | num     |   338 | DA DECIDERE
#     CTX_RH_MIDDLETEMPORAL_VOLUME | num     |   434 | DA DECIDERE
#     CTX_RH_PARACENTRAL_SUVR  | num     |   309 | DA DECIDERE
#     CTX_RH_PARACENTRAL_VOLUME | num     |   406 | DA DECIDERE
#     CTX_RH_PARAHIPPOCAMPAL_SUVR | num     |   364 | DA DECIDERE
#     CTX_RH_PARAHIPPOCAMPAL_VOLUME | num     |   365 | DA DECIDERE
#     CTX_RH_PARSOPERCULARIS_SUVR | num     |   318 | DA DECIDERE
#     CTX_RH_PARSOPERCULARIS_VOLUME | num     |   414 | DA DECIDERE
#     CTX_RH_PARSORBITALIS_SUVR | num     |   315 | DA DECIDERE
#     CTX_RH_PARSORBITALIS_VOLUME | num     |   373 | DA DECIDERE
#     CTX_RH_PARSTRIANGULARIS_SUVR | num     |   313 | DA DECIDERE
#     CTX_RH_PARSTRIANGULARIS_VOLUME | num     |   416 | DA DECIDERE
#     CTX_RH_PERICALCARINE_SUVR | num     |   328 | DA DECIDERE
#     CTX_RH_PERICALCARINE_VOLUME | num     |   410 | DA DECIDERE
#     CTX_RH_POSTCENTRAL_SUVR  | num     |   290 | DA DECIDERE
#     CTX_RH_POSTCENTRAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_RH_POSTERIORCINGULATE_SUVR | num     |   335 | DA DECIDERE
#     CTX_RH_POSTERIORCINGULATE_VOLUME | num     |   403 | DA DECIDERE
#     CTX_RH_PRECENTRAL_SUVR   | num     |   297 | DA DECIDERE
#     CTX_RH_PRECENTRAL_VOLUME | num     |   433 | DA DECIDERE
#     CTX_RH_PRECUNEUS_SUVR    | num     |   335 | DA DECIDERE
#     CTX_RH_PRECUNEUS_VOLUME  | num     |   436 | DA DECIDERE
#     CTX_RH_ROSTRALANTERIORCINGULATE_SUVR | num     |   300 | DA DECIDERE
#     CTX_RH_ROSTRALANTERIORCINGULATE_VOLUME | num     |   392 | DA DECIDERE
#     CTX_RH_ROSTRALMIDDLEFRONTAL_SUVR | num     |   323 | DA DECIDERE
#     CTX_RH_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   448 | DA DECIDERE
#     CTX_RH_SUPERIORFRONTAL_SUVR | num     |   319 | DA DECIDERE
#     CTX_RH_SUPERIORFRONTAL_VOLUME | num     |   447 | DA DECIDERE
#     CTX_RH_SUPERIORPARIETAL_SUVR | num     |   332 | DA DECIDERE
#     CTX_RH_SUPERIORPARIETAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_RH_SUPERIORTEMPORAL_SUVR | num     |   332 | DA DECIDERE
#     CTX_RH_SUPERIORTEMPORAL_VOLUME | num     |   442 | DA DECIDERE
#     CTX_RH_SUPRAMARGINAL_SUVR | num     |   335 | DA DECIDERE
#     CTX_RH_SUPRAMARGINAL_VOLUME | num     |   440 | DA DECIDERE
#     CTX_RH_TEMPORALPOLE_SUVR | num     |   366 | DA DECIDERE
#     CTX_RH_TEMPORALPOLE_VOLUME | num     |   399 | DA DECIDERE
#     CTX_RH_TRANSVERSETEMPORAL_SUVR | num     |   346 | DA DECIDERE
#     CTX_RH_TRANSVERSETEMPORAL_VOLUME | num     |   312 | DA DECIDERE
#     LEFT_ACCUMBENS_AREA_SUVR | num     |   425 | DA DECIDERE
#     LEFT_ACCUMBENS_AREA_VOLUME | num     |   243 | DA DECIDERE
#     LEFT_AMYGDALA_SUVR       | num     |   390 | DA DECIDERE
#     LEFT_AMYGDALA_VOLUME     | num     |   364 | DA DECIDERE
#     LEFT_CAUDATE_SUVR        | num     |   387 | DA DECIDERE
#     LEFT_CAUDATE_VOLUME      | num     |   410 | DA DECIDERE
#     LEFT_CEREBELLUM_CORTEX_SUVR | num     |   125 | DA DECIDERE
#     LEFT_CEREBELLUM_CORTEX_VOLUME | num     |   456 | DA DECIDERE
#     LEFT_CEREBELLUM_WHITE_MATTER_SUVR | num     |   298 | DA DECIDERE
#     LEFT_CEREBELLUM_WHITE_MATTER_VOLUME | num     |   450 | DA DECIDERE
#     LEFT_CEREBRAL_WHITE_MATTER_SUVR | num     |   327 | DA DECIDERE
#     LEFT_CEREBRAL_WHITE_MATTER_VOLUME | num     |   462 | DA DECIDERE
#     LEFT_CHOROID_PLEXUS_SUVR | num     |   473 | DA DECIDERE
#     LEFT_CHOROID_PLEXUS_VOLUME | num     |   348 | DA DECIDERE
#     LEFT_HIPPOCAMPUS_SUVR    | num     |   366 | DA DECIDERE
#     LEFT_HIPPOCAMPUS_VOLUME  | num     |   413 | DA DECIDERE
#     LEFT_INF_LAT_VENT_SUVR   | num     |   429 | DA DECIDERE
#     LEFT_INF_LAT_VENT_VOLUME | num     |   403 | DA DECIDERE
#     LEFT_LATERAL_VENTRICLE_SUVR | num     |   256 | DA DECIDERE
#     LEFT_LATERAL_VENTRICLE_VOLUME | num     |   462 | DA DECIDERE
#     LEFT_PALLIDUM_SUVR       | num     |   396 | DA DECIDERE
#     LEFT_PALLIDUM_VOLUME     | num     |   357 | DA DECIDERE
#     LEFT_PUTAMEN_SUVR        | num     |   379 | DA DECIDERE
#     LEFT_PUTAMEN_VOLUME      | num     |   420 | DA DECIDERE
#     LEFT_THALAMUS_PROPER_SUVR | num     |   313 | DA DECIDERE
#     LEFT_THALAMUS_PROPER_VOLUME | num     |   422 | DA DECIDERE
#     LEFT_VENTRALDC_SUVR      | num     |   331 | DA DECIDERE
#     LEFT_VENTRALDC_VOLUME    | num     |   401 | DA DECIDERE
#     LEFT_VESSEL_SUVR         | vuota   |     0 | DA DECIDERE
#     LEFT_VESSEL_VOLUME       | num     |    98 | DA DECIDERE
#     RIGHT_ACCUMBENS_AREA_SUVR | num     |   415 | DA DECIDERE
#     RIGHT_ACCUMBENS_AREA_VOLUME | num     |   256 | DA DECIDERE
#     RIGHT_AMYGDALA_SUVR      | num     |   385 | DA DECIDERE
#     RIGHT_AMYGDALA_VOLUME    | num     |   372 | DA DECIDERE
#     RIGHT_CAUDATE_SUVR       | num     |   383 | DA DECIDERE
#     RIGHT_CAUDATE_VOLUME     | num     |   403 | DA DECIDERE
#     RIGHT_CEREBELLUM_CORTEX_SUVR | num     |   124 | DA DECIDERE
#     RIGHT_CEREBELLUM_CORTEX_VOLUME | num     |   459 | DA DECIDERE
#     RIGHT_CEREBELLUM_WHITE_MATTER_SUVR | num     |   298 | DA DECIDERE
#     RIGHT_CEREBELLUM_WHITE_MATTER_VOLUME | num     |   441 | DA DECIDERE
#     RIGHT_CEREBRAL_WHITE_MATTER_SUVR | num     |   328 | DA DECIDERE
#     RIGHT_CEREBRAL_WHITE_MATTER_VOLUME | num     |   460 | DA DECIDERE
#     RIGHT_CHOROID_PLEXUS_SUVR | num     |   465 | DA DECIDERE
#     RIGHT_CHOROID_PLEXUS_VOLUME | num     |   353 | DA DECIDERE
#     RIGHT_HIPPOCAMPUS_SUVR   | num     |   356 | DA DECIDERE
#     RIGHT_HIPPOCAMPUS_VOLUME | num     |   413 | DA DECIDERE
#     RIGHT_INF_LAT_VENT_SUVR  | num     |   429 | DA DECIDERE
#     RIGHT_INF_LAT_VENT_VOLUME | num     |   397 | DA DECIDERE
#     RIGHT_LATERAL_VENTRICLE_SUVR | num     |   256 | DA DECIDERE
#     RIGHT_LATERAL_VENTRICLE_VOLUME | num     |   458 | DA DECIDERE
#     RIGHT_PALLIDUM_SUVR      | num     |   391 | DA DECIDERE
#     RIGHT_PALLIDUM_VOLUME    | num     |   371 | DA DECIDERE
#     RIGHT_PUTAMEN_SUVR       | num     |   386 | DA DECIDERE
#     RIGHT_PUTAMEN_VOLUME     | num     |   419 | DA DECIDERE
#     RIGHT_THALAMUS_PROPER_SUVR | num     |   300 | DA DECIDERE
#     RIGHT_THALAMUS_PROPER_VOLUME | num     |   420 | DA DECIDERE
#     RIGHT_VENTRALDC_SUVR     | num     |   331 | DA DECIDERE
#     RIGHT_VENTRALDC_VOLUME   | num     |   401 | DA DECIDERE
#     RIGHT_VESSEL_SUVR        | vuota   |     0 | DA DECIDERE
#     RIGHT_VESSEL_VOLUME      | num     |    89 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UCBERKELEY_TAUPVC_6MM = DatasetConfig(
    file_code="UCBERKELEY_TAUPVC_6MM",                          # <-- VERIFICA
    source="UCBERKELEY_TAUPVC_6MM_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['pet'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="SCANDATE",          # preferenza ADNI (alt: ['PROCESSDATE', 'update_stamp']) VERIFICA
    # 326 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['TRACER', 'TRACER_SUVR_WARNING', 'META_TEMPORAL_SUVR', 'META_TEMPORAL_VOLUME', 'CTX_ENTORHINAL_SUVR', 'CTX_ENTORHINAL_VOLUME', 'INFERIORCEREBELLUM_SUVR', 'INFERIORCEREBELLUM_VOLUME', 'CEREBRAL_WHITE_MATTER_SUVR', 'CEREBRAL_WHITE_MATTER_VOLUME', 'BRAINSTEM_SUVR', 'BRAINSTEM_VOLUME', 'CC_ANTERIOR_SUVR', 'CC_ANTERIOR_VOLUME', 'CC_CENTRAL_SUVR', 'CC_CENTRAL_VOLUME', 'CC_MID_ANTERIOR_SUVR', 'CC_MID_ANTERIOR_VOLUME', 'CC_MID_POSTERIOR_SUVR', 'CC_MID_POSTERIOR_VOLUME', 'CC_POSTERIOR_SUVR', 'CC_POSTERIOR_VOLUME', 'CSF_SUVR', 'CSF_VOLUME', 'VENTRICLE_3RD_SUVR', 'VENTRICLE_3RD_VOLUME', 'VENTRICLE_4TH_SUVR', 'VENTRICLE_4TH_VOLUME', 'VENTRICLE_5TH_SUVR', 'VENTRICLE_5TH_VOLUME', 'WM_HYPOINTENSITIES_SUVR', 'WM_HYPOINTENSITIES_VOLUME', 'NON_WM_HYPOINTENSITIES_SUVR', 'NON_WM_HYPOINTENSITIES_VOLUME', 'CTX_BANKSSTS_SUVR', 'CTX_BANKSSTS_VOLUME', 'CTX_CAUDALANTERIORCINGULATE_SUVR', 'CTX_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_CUNEUS_SUVR', 'CTX_CUNEUS_VOLUME', 'CTX_FRONTALPOLE_SUVR', 'CTX_FRONTALPOLE_VOLUME', 'CTX_FUSIFORM_SUVR', 'CTX_FUSIFORM_VOLUME', 'CTX_INFERIORPARIETAL_SUVR', 'CTX_INFERIORPARIETAL_VOLUME', 'CTX_INFERIORTEMPORAL_SUVR', 'CTX_INFERIORTEMPORAL_VOLUME', 'CTX_INSULA_SUVR', 'CTX_INSULA_VOLUME', 'CTX_ISTHMUSCINGULATE_SUVR', 'CTX_ISTHMUSCINGULATE_VOLUME', 'CTX_LATERALOCCIPITAL_SUVR', 'CTX_LATERALOCCIPITAL_VOLUME', 'CTX_LATERALORBITOFRONTAL_SUVR', 'CTX_LATERALORBITOFRONTAL_VOLUME', 'CTX_LINGUAL_SUVR', 'CTX_LINGUAL_VOLUME', 'CTX_MEDIALORBITOFRONTAL_SUVR', 'CTX_MEDIALORBITOFRONTAL_VOLUME', 'CTX_MIDDLETEMPORAL_SUVR', 'CTX_MIDDLETEMPORAL_VOLUME', 'CTX_PARACENTRAL_SUVR', 'CTX_PARACENTRAL_VOLUME', 'CTX_PARAHIPPOCAMPAL_SUVR', 'CTX_PARAHIPPOCAMPAL_VOLUME', 'CTX_PARSOPERCULARIS_SUVR', 'CTX_PARSOPERCULARIS_VOLUME', 'CTX_PARSORBITALIS_SUVR', 'CTX_PARSORBITALIS_VOLUME', 'CTX_PARSTRIANGULARIS_SUVR', 'CTX_PARSTRIANGULARIS_VOLUME', 'CTX_PERICALCARINE_SUVR', 'CTX_PERICALCARINE_VOLUME', 'CTX_POSTCENTRAL_SUVR', 'CTX_POSTCENTRAL_VOLUME', 'CTX_POSTERIORCINGULATE_SUVR', 'CTX_POSTERIORCINGULATE_VOLUME', 'CTX_PRECENTRAL_SUVR', 'CTX_PRECENTRAL_VOLUME', 'CTX_PRECUNEUS_SUVR', 'CTX_PRECUNEUS_VOLUME', 'CTX_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_SUPERIORFRONTAL_SUVR', 'CTX_SUPERIORFRONTAL_VOLUME', 'CTX_SUPERIORPARIETAL_SUVR', 'CTX_SUPERIORPARIETAL_VOLUME', 'CTX_SUPERIORTEMPORAL_SUVR', 'CTX_SUPERIORTEMPORAL_VOLUME', 'CTX_SUPRAMARGINAL_SUVR', 'CTX_SUPRAMARGINAL_VOLUME', 'CTX_TEMPORALPOLE_SUVR', 'CTX_TEMPORALPOLE_VOLUME', 'CTX_TRANSVERSETEMPORAL_SUVR', 'CTX_TRANSVERSETEMPORAL_VOLUME', 'ACCUMBENS_AREA_SUVR', 'ACCUMBENS_AREA_VOLUME', 'AMYGDALA_SUVR', 'AMYGDALA_VOLUME', 'CAUDATE_SUVR', 'CAUDATE_VOLUME', 'CEREBELLUM_CORTEX_SUVR', 'CEREBELLUM_CORTEX_VOLUME', 'CEREBELLUM_WHITE_MATTER_SUVR', 'CEREBELLUM_WHITE_MATTER_VOLUME', 'CHOROID_PLEXUS_SUVR', 'CHOROID_PLEXUS_VOLUME', 'HIPPOCAMPUS_SUVR', 'HIPPOCAMPUS_VOLUME', 'OPTIC_CHIASM_SUVR', 'OPTIC_CHIASM_VOLUME', 'INF_LAT_VENT_SUVR', 'INF_LAT_VENT_VOLUME', 'LATERAL_VENTRICLE_SUVR', 'LATERAL_VENTRICLE_VOLUME', 'PALLIDUM_SUVR', 'PALLIDUM_VOLUME', 'PUTAMEN_SUVR', 'PUTAMEN_VOLUME', 'THALAMUS_PROPER_SUVR', 'THALAMUS_PROPER_VOLUME', 'VENTRALDC_SUVR', 'VENTRALDC_VOLUME', 'VESSEL_SUVR', 'VESSEL_VOLUME', 'CTX_LH_BANKSSTS_SUVR', 'CTX_LH_BANKSSTS_VOLUME', 'CTX_LH_CAUDALANTERIORCINGULATE_SUVR', 'CTX_LH_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_LH_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_LH_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_LH_CUNEUS_SUVR', 'CTX_LH_CUNEUS_VOLUME', 'CTX_LH_ENTORHINAL_SUVR', 'CTX_LH_ENTORHINAL_VOLUME', 'CTX_LH_FRONTALPOLE_SUVR', 'CTX_LH_FRONTALPOLE_VOLUME', 'CTX_LH_FUSIFORM_SUVR', 'CTX_LH_FUSIFORM_VOLUME', 'CTX_LH_INFERIORPARIETAL_SUVR', 'CTX_LH_INFERIORPARIETAL_VOLUME', 'CTX_LH_INFERIORTEMPORAL_SUVR', 'CTX_LH_INFERIORTEMPORAL_VOLUME', 'CTX_LH_INSULA_SUVR', 'CTX_LH_INSULA_VOLUME', 'CTX_LH_ISTHMUSCINGULATE_SUVR', 'CTX_LH_ISTHMUSCINGULATE_VOLUME', 'CTX_LH_LATERALOCCIPITAL_SUVR', 'CTX_LH_LATERALOCCIPITAL_VOLUME', 'CTX_LH_LATERALORBITOFRONTAL_SUVR', 'CTX_LH_LATERALORBITOFRONTAL_VOLUME', 'CTX_LH_LINGUAL_SUVR', 'CTX_LH_LINGUAL_VOLUME', 'CTX_LH_MEDIALORBITOFRONTAL_SUVR', 'CTX_LH_MEDIALORBITOFRONTAL_VOLUME', 'CTX_LH_MIDDLETEMPORAL_SUVR', 'CTX_LH_MIDDLETEMPORAL_VOLUME', 'CTX_LH_PARACENTRAL_SUVR', 'CTX_LH_PARACENTRAL_VOLUME', 'CTX_LH_PARAHIPPOCAMPAL_SUVR', 'CTX_LH_PARAHIPPOCAMPAL_VOLUME', 'CTX_LH_PARSOPERCULARIS_SUVR', 'CTX_LH_PARSOPERCULARIS_VOLUME', 'CTX_LH_PARSORBITALIS_SUVR', 'CTX_LH_PARSORBITALIS_VOLUME', 'CTX_LH_PARSTRIANGULARIS_SUVR', 'CTX_LH_PARSTRIANGULARIS_VOLUME', 'CTX_LH_PERICALCARINE_SUVR', 'CTX_LH_PERICALCARINE_VOLUME', 'CTX_LH_POSTCENTRAL_SUVR', 'CTX_LH_POSTCENTRAL_VOLUME', 'CTX_LH_POSTERIORCINGULATE_SUVR', 'CTX_LH_POSTERIORCINGULATE_VOLUME', 'CTX_LH_PRECENTRAL_SUVR', 'CTX_LH_PRECENTRAL_VOLUME', 'CTX_LH_PRECUNEUS_SUVR', 'CTX_LH_PRECUNEUS_VOLUME', 'CTX_LH_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_LH_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_LH_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_LH_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_LH_SUPERIORFRONTAL_SUVR', 'CTX_LH_SUPERIORFRONTAL_VOLUME', 'CTX_LH_SUPERIORPARIETAL_SUVR', 'CTX_LH_SUPERIORPARIETAL_VOLUME', 'CTX_LH_SUPERIORTEMPORAL_SUVR', 'CTX_LH_SUPERIORTEMPORAL_VOLUME', 'CTX_LH_SUPRAMARGINAL_SUVR', 'CTX_LH_SUPRAMARGINAL_VOLUME', 'CTX_LH_TEMPORALPOLE_SUVR', 'CTX_LH_TEMPORALPOLE_VOLUME', 'CTX_LH_TRANSVERSETEMPORAL_SUVR', 'CTX_LH_TRANSVERSETEMPORAL_VOLUME', 'CTX_RH_BANKSSTS_SUVR', 'CTX_RH_BANKSSTS_VOLUME', 'CTX_RH_CAUDALANTERIORCINGULATE_SUVR', 'CTX_RH_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_RH_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_RH_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_RH_CUNEUS_SUVR', 'CTX_RH_CUNEUS_VOLUME', 'CTX_RH_ENTORHINAL_SUVR', 'CTX_RH_ENTORHINAL_VOLUME', 'CTX_RH_FRONTALPOLE_SUVR', 'CTX_RH_FRONTALPOLE_VOLUME', 'CTX_RH_FUSIFORM_SUVR', 'CTX_RH_FUSIFORM_VOLUME', 'CTX_RH_INFERIORPARIETAL_SUVR', 'CTX_RH_INFERIORPARIETAL_VOLUME', 'CTX_RH_INFERIORTEMPORAL_SUVR', 'CTX_RH_INFERIORTEMPORAL_VOLUME', 'CTX_RH_INSULA_SUVR', 'CTX_RH_INSULA_VOLUME', 'CTX_RH_ISTHMUSCINGULATE_SUVR', 'CTX_RH_ISTHMUSCINGULATE_VOLUME', 'CTX_RH_LATERALOCCIPITAL_SUVR', 'CTX_RH_LATERALOCCIPITAL_VOLUME', 'CTX_RH_LATERALORBITOFRONTAL_SUVR', 'CTX_RH_LATERALORBITOFRONTAL_VOLUME', 'CTX_RH_LINGUAL_SUVR', 'CTX_RH_LINGUAL_VOLUME', 'CTX_RH_MEDIALORBITOFRONTAL_SUVR', 'CTX_RH_MEDIALORBITOFRONTAL_VOLUME', 'CTX_RH_MIDDLETEMPORAL_SUVR', 'CTX_RH_MIDDLETEMPORAL_VOLUME', 'CTX_RH_PARACENTRAL_SUVR', 'CTX_RH_PARACENTRAL_VOLUME', 'CTX_RH_PARAHIPPOCAMPAL_SUVR', 'CTX_RH_PARAHIPPOCAMPAL_VOLUME', 'CTX_RH_PARSOPERCULARIS_SUVR', 'CTX_RH_PARSOPERCULARIS_VOLUME', 'CTX_RH_PARSORBITALIS_SUVR', 'CTX_RH_PARSORBITALIS_VOLUME', 'CTX_RH_PARSTRIANGULARIS_SUVR', 'CTX_RH_PARSTRIANGULARIS_VOLUME', 'CTX_RH_PERICALCARINE_SUVR', 'CTX_RH_PERICALCARINE_VOLUME', 'CTX_RH_POSTCENTRAL_SUVR', 'CTX_RH_POSTCENTRAL_VOLUME', 'CTX_RH_POSTERIORCINGULATE_SUVR', 'CTX_RH_POSTERIORCINGULATE_VOLUME', 'CTX_RH_PRECENTRAL_SUVR', 'CTX_RH_PRECENTRAL_VOLUME', 'CTX_RH_PRECUNEUS_SUVR', 'CTX_RH_PRECUNEUS_VOLUME', 'CTX_RH_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_RH_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_RH_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_RH_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_RH_SUPERIORFRONTAL_SUVR', 'CTX_RH_SUPERIORFRONTAL_VOLUME', 'CTX_RH_SUPERIORPARIETAL_SUVR', 'CTX_RH_SUPERIORPARIETAL_VOLUME', 'CTX_RH_SUPERIORTEMPORAL_SUVR', 'CTX_RH_SUPERIORTEMPORAL_VOLUME', 'CTX_RH_SUPRAMARGINAL_SUVR', 'CTX_RH_SUPRAMARGINAL_VOLUME', 'CTX_RH_TEMPORALPOLE_SUVR', 'CTX_RH_TEMPORALPOLE_VOLUME', 'CTX_RH_TRANSVERSETEMPORAL_SUVR', 'CTX_RH_TRANSVERSETEMPORAL_VOLUME', 'LEFT_ACCUMBENS_AREA_SUVR', 'LEFT_ACCUMBENS_AREA_VOLUME', 'LEFT_AMYGDALA_SUVR', 'LEFT_AMYGDALA_VOLUME', 'LEFT_CAUDATE_SUVR', 'LEFT_CAUDATE_VOLUME', 'LEFT_CEREBELLUM_CORTEX_SUVR', 'LEFT_CEREBELLUM_CORTEX_VOLUME', 'LEFT_CEREBELLUM_WHITE_MATTER_SUVR', 'LEFT_CEREBELLUM_WHITE_MATTER_VOLUME', 'LEFT_CEREBRAL_WHITE_MATTER_SUVR', 'LEFT_CEREBRAL_WHITE_MATTER_VOLUME', 'LEFT_CHOROID_PLEXUS_SUVR', 'LEFT_CHOROID_PLEXUS_VOLUME', 'LEFT_HIPPOCAMPUS_SUVR', 'LEFT_HIPPOCAMPUS_VOLUME', 'LEFT_INF_LAT_VENT_SUVR', 'LEFT_INF_LAT_VENT_VOLUME', 'LEFT_LATERAL_VENTRICLE_SUVR', 'LEFT_LATERAL_VENTRICLE_VOLUME', 'LEFT_PALLIDUM_SUVR', 'LEFT_PALLIDUM_VOLUME', 'LEFT_PUTAMEN_SUVR', 'LEFT_PUTAMEN_VOLUME', 'LEFT_THALAMUS_PROPER_SUVR', 'LEFT_THALAMUS_PROPER_VOLUME', 'LEFT_VENTRALDC_SUVR', 'LEFT_VENTRALDC_VOLUME', 'LEFT_VESSEL_SUVR', 'LEFT_VESSEL_VOLUME', 'RIGHT_ACCUMBENS_AREA_SUVR', 'RIGHT_ACCUMBENS_AREA_VOLUME', 'RIGHT_AMYGDALA_SUVR', 'RIGHT_AMYGDALA_VOLUME', 'RIGHT_CAUDATE_SUVR', 'RIGHT_CAUDATE_VOLUME', 'RIGHT_CEREBELLUM_CORTEX_SUVR', 'RIGHT_CEREBELLUM_CORTEX_VOLUME', 'RIGHT_CEREBELLUM_WHITE_MATTER_SUVR', 'RIGHT_CEREBELLUM_WHITE_MATTER_VOLUME', 'RIGHT_CEREBRAL_WHITE_MATTER_SUVR', 'RIGHT_CEREBRAL_WHITE_MATTER_VOLUME', 'RIGHT_CHOROID_PLEXUS_SUVR', 'RIGHT_CHOROID_PLEXUS_VOLUME', 'RIGHT_HIPPOCAMPUS_SUVR', 'RIGHT_HIPPOCAMPUS_VOLUME', 'RIGHT_INF_LAT_VENT_SUVR', 'RIGHT_INF_LAT_VENT_VOLUME', 'RIGHT_LATERAL_VENTRICLE_SUVR', 'RIGHT_LATERAL_VENTRICLE_VOLUME', 'RIGHT_PALLIDUM_SUVR', 'RIGHT_PALLIDUM_VOLUME', 'RIGHT_PUTAMEN_SUVR', 'RIGHT_PUTAMEN_VOLUME', 'RIGHT_THALAMUS_PROPER_SUVR', 'RIGHT_THALAMUS_PROPER_VOLUME', 'RIGHT_VENTRALDC_SUVR', 'RIGHT_VENTRALDC_VOLUME', 'RIGHT_VESSEL_SUVR', 'RIGHT_VESSEL_VOLUME']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCBERKELEY_TAU_6MM
#   source: UCBERKELEY_TAU_6MM_28Oct2025.csv   |   righe campionate: 500   |   colonne: 339
#   INDIZIO categoria dal nome (NON deciso): ['pet']
#   ignorate 3 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   262 | cand. ID
#     RID                      | num     |   262 | cand. ID
#     VISCODE                  | cat/str |     9 | cand. VISITA
#     VISCODE2                 | cat/str |    27 | cand. VISITA
#     SCANDATE                 | date    |   387 | cand. DATA
#     PROCESSDATE              | date    |    30 | cand. DATA
#     IMAGE_RESOLUTION         | cat/str |     1 | DA DECIDERE
#     TRACER                   | cat/str |     1 | DA DECIDERE
#     TRACER_SUVR_WARNING      | cat/str |     1 | DA DECIDERE
#     META_TEMPORAL_SUVR       | num     |   311 | DA DECIDERE
#     META_TEMPORAL_VOLUME     | num     |   457 | DA DECIDERE
#     CTX_ENTORHINAL_SUVR      | num     |   354 | DA DECIDERE
#     CTX_ENTORHINAL_VOLUME    | num     |   424 | DA DECIDERE
#     INFERIORCEREBELLUM_SUVR  | num     |     1 | DA DECIDERE
#     INFERIORCEREBELLUM_VOLUME | num     |   461 | DA DECIDERE
#     ERODED_SUBCORTICALWM_SUVR | num     |   306 | DA DECIDERE
#     ERODED_SUBCORTICALWM_VOLUME | num     |   462 | DA DECIDERE
#     BRAINSTEM_SUVR           | num     |   254 | DA DECIDERE
#     BRAINSTEM_VOLUME         | num     |   452 | DA DECIDERE
#     CC_ANTERIOR_SUVR         | num     |   329 | DA DECIDERE
#     CC_ANTERIOR_VOLUME       | num     |   323 | DA DECIDERE
#     CC_CENTRAL_SUVR          | num     |   300 | DA DECIDERE
#     CC_CENTRAL_VOLUME        | num     |   256 | DA DECIDERE
#     CC_MID_ANTERIOR_SUVR     | num     |   316 | DA DECIDERE
#     CC_MID_ANTERIOR_VOLUME   | num     |   257 | DA DECIDERE
#     CC_MID_POSTERIOR_SUVR    | num     |   324 | DA DECIDERE
#     CC_MID_POSTERIOR_VOLUME  | num     |   289 | DA DECIDERE
#     CC_POSTERIOR_SUVR        | num     |   299 | DA DECIDERE
#     CC_POSTERIOR_VOLUME      | num     |   307 | DA DECIDERE
#     CSF_SUVR                 | num     |   324 | DA DECIDERE
#     CSF_VOLUME               | num     |   382 | DA DECIDERE
#     VENTRICLE_3RD_SUVR       | num     |   316 | DA DECIDERE
#     VENTRICLE_3RD_VOLUME     | num     |   415 | DA DECIDERE
#     VENTRICLE_4TH_SUVR       | num     |   308 | DA DECIDERE
#     VENTRICLE_4TH_VOLUME     | num     |   416 | DA DECIDERE
#     VENTRICLE_5TH_SUVR       | num     |     6 | DA DECIDERE
#     VENTRICLE_5TH_VOLUME     | num     |     6 | DA DECIDERE
#     WM_HYPOINTENSITIES_SUVR  | num     |   296 | DA DECIDERE
#     WM_HYPOINTENSITIES_VOLUME | num     |   450 | DA DECIDERE
#     NON_WM_HYPOINTENSITIES_SUVR | num     |    43 | DA DECIDERE
#     NON_WM_HYPOINTENSITIES_VOLUME | num     |     9 | DA DECIDERE
#     CTX_BANKSSTS_SUVR        | num     |   311 | DA DECIDERE
#     CTX_BANKSSTS_VOLUME      | num     |   423 | DA DECIDERE
#     CTX_CAUDALANTERIORCINGULATE_SUVR | num     |   297 | DA DECIDERE
#     CTX_CAUDALANTERIORCINGULATE_VOLUME | num     |   410 | DA DECIDERE
#     CTX_CAUDALMIDDLEFRONTAL_SUVR | num     |   295 | DA DECIDERE
#     CTX_CAUDALMIDDLEFRONTAL_VOLUME | num     |   448 | DA DECIDERE
#     CTX_CUNEUS_SUVR          | num     |   277 | DA DECIDERE
#     CTX_CUNEUS_VOLUME        | num     |   433 | DA DECIDERE
#     CTX_FRONTALPOLE_SUVR     | num     |   310 | DA DECIDERE
#     CTX_FRONTALPOLE_VOLUME   | num     |   392 | DA DECIDERE
#     CTX_FUSIFORM_SUVR        | num     |   312 | DA DECIDERE
#     CTX_FUSIFORM_VOLUME      | num     |   449 | DA DECIDERE
#     CTX_INFERIORPARIETAL_SUVR | num     |   305 | DA DECIDERE
#     CTX_INFERIORPARIETAL_VOLUME | num     |   455 | DA DECIDERE
#     CTX_INFERIORTEMPORAL_SUVR | num     |   323 | DA DECIDERE
#     CTX_INFERIORTEMPORAL_VOLUME | num     |   456 | DA DECIDERE
#     CTX_INSULA_SUVR          | num     |   302 | DA DECIDERE
#     CTX_INSULA_VOLUME        | num     |   436 | DA DECIDERE
#     CTX_ISTHMUSCINGULATE_SUVR | num     |   309 | DA DECIDERE
#     CTX_ISTHMUSCINGULATE_VOLUME | num     |   422 | DA DECIDERE
#     CTX_LATERALOCCIPITAL_SUVR | num     |   321 | DA DECIDERE
#     CTX_LATERALOCCIPITAL_VOLUME | num     |   455 | DA DECIDERE
#     CTX_LATERALORBITOFRONTAL_SUVR | num     |   304 | DA DECIDERE
#     CTX_LATERALORBITOFRONTAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_LINGUAL_SUVR         | num     |   291 | DA DECIDERE
#     CTX_LINGUAL_VOLUME       | num     |   447 | DA DECIDERE
#     CTX_MEDIALORBITOFRONTAL_SUVR | num     |   306 | DA DECIDERE
#     CTX_MEDIALORBITOFRONTAL_VOLUME | num     |   437 | DA DECIDERE
#     CTX_MIDDLETEMPORAL_SUVR  | num     |   309 | DA DECIDERE
#     CTX_MIDDLETEMPORAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_PARACENTRAL_SUVR     | num     |   285 | DA DECIDERE
#     CTX_PARACENTRAL_VOLUME   | num     |   423 | DA DECIDERE
#     CTX_PARAHIPPOCAMPAL_SUVR | num     |   322 | DA DECIDERE
#     CTX_PARAHIPPOCAMPAL_VOLUME | num     |   399 | DA DECIDERE
#     CTX_PARSOPERCULARIS_SUVR | num     |   295 | DA DECIDERE
#     CTX_PARSOPERCULARIS_VOLUME | num     |   438 | DA DECIDERE
#     CTX_PARSORBITALIS_SUVR   | num     |   304 | DA DECIDERE
#     CTX_PARSORBITALIS_VOLUME | num     |   401 | DA DECIDERE
#     CTX_PARSTRIANGULARIS_SUVR | num     |   287 | DA DECIDERE
#     CTX_PARSTRIANGULARIS_VOLUME | num     |   430 | DA DECIDERE
#     CTX_PERICALCARINE_SUVR   | num     |   270 | DA DECIDERE
#     CTX_PERICALCARINE_VOLUME | num     |   436 | DA DECIDERE
#     CTX_POSTCENTRAL_SUVR     | num     |   271 | DA DECIDERE
#     CTX_POSTCENTRAL_VOLUME   | num     |   456 | DA DECIDERE
#     CTX_POSTERIORCINGULATE_SUVR | num     |   311 | DA DECIDERE
#     CTX_POSTERIORCINGULATE_VOLUME | num     |   416 | DA DECIDERE
#     CTX_PRECENTRAL_SUVR      | num     |   272 | DA DECIDERE
#     CTX_PRECENTRAL_VOLUME    | num     |   452 | DA DECIDERE
#     CTX_PRECUNEUS_SUVR       | num     |   300 | DA DECIDERE
#     CTX_PRECUNEUS_VOLUME     | num     |   439 | DA DECIDERE
#     CTX_ROSTRALANTERIORCINGULATE_SUVR | num     |   308 | DA DECIDERE
#     CTX_ROSTRALANTERIORCINGULATE_VOLUME | num     |   425 | DA DECIDERE
#     CTX_ROSTRALMIDDLEFRONTAL_SUVR | num     |   282 | DA DECIDERE
#     CTX_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   453 | DA DECIDERE
#     CTX_SUPERIORFRONTAL_SUVR | num     |   280 | DA DECIDERE
#     CTX_SUPERIORFRONTAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_SUPERIORPARIETAL_SUVR | num     |   291 | DA DECIDERE
#     CTX_SUPERIORPARIETAL_VOLUME | num     |   454 | DA DECIDERE
#     CTX_SUPERIORTEMPORAL_SUVR | num     |   295 | DA DECIDERE
#     CTX_SUPERIORTEMPORAL_VOLUME | num     |   445 | DA DECIDERE
#     CTX_SUPRAMARGINAL_SUVR   | num     |   293 | DA DECIDERE
#     CTX_SUPRAMARGINAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_TEMPORALPOLE_SUVR    | num     |   330 | DA DECIDERE
#     CTX_TEMPORALPOLE_VOLUME  | num     |   435 | DA DECIDERE
#     CTX_TRANSVERSETEMPORAL_SUVR | num     |   302 | DA DECIDERE
#     CTX_TRANSVERSETEMPORAL_VOLUME | num     |   379 | DA DECIDERE
#     ACCUMBENS_AREA_SUVR      | num     |   334 | DA DECIDERE
#     ACCUMBENS_AREA_VOLUME    | num     |   325 | DA DECIDERE
#     AMYGDALA_SUVR            | num     |   360 | DA DECIDERE
#     AMYGDALA_VOLUME          | num     |   405 | DA DECIDERE
#     CAUDATE_SUVR             | num     |   335 | DA DECIDERE
#     CAUDATE_VOLUME           | num     |   430 | DA DECIDERE
#     CEREBELLUM_CORTEX_SUVR   | num     |    97 | DA DECIDERE
#     CEREBELLUM_CORTEX_VOLUME | num     |   461 | DA DECIDERE
#     CEREBELLUM_WHITE_MATTER_SUVR | num     |   237 | DA DECIDERE
#     CEREBELLUM_WHITE_MATTER_VOLUME | num     |   454 | DA DECIDERE
#     CEREBRAL_WHITE_MATTER_SUVR | num     |   302 | DA DECIDERE
#     CEREBRAL_WHITE_MATTER_VOLUME | num     |   462 | DA DECIDERE
#     CHOROID_PLEXUS_SUVR      | num     |   396 | DA DECIDERE
#     CHOROID_PLEXUS_VOLUME    | num     |   400 | DA DECIDERE
#     HIPPOCAMPUS_SUVR         | num     |   350 | DA DECIDERE
#     HIPPOCAMPUS_VOLUME       | num     |   426 | DA DECIDERE
#     OPTIC_CHIASM_SUVR        | num     |   287 | DA DECIDERE
#     OPTIC_CHIASM_VOLUME      | num     |   151 | DA DECIDERE
#     INF_LAT_VENT_SUVR        | num     |   359 | DA DECIDERE
#     INF_LAT_VENT_VOLUME      | num     |   425 | DA DECIDERE
#     LATERAL_VENTRICLE_SUVR   | num     |   331 | DA DECIDERE
#     LATERAL_VENTRICLE_VOLUME | num     |   460 | DA DECIDERE
#     PALLIDUM_SUVR            | num     |   368 | DA DECIDERE
#     PALLIDUM_VOLUME          | num     |   404 | DA DECIDERE
#     PUTAMEN_SUVR             | num     |   350 | DA DECIDERE
#     PUTAMEN_VOLUME           | num     |   429 | DA DECIDERE
#     THALAMUS_PROPER_SUVR     | num     |   295 | DA DECIDERE
#     THALAMUS_PROPER_VOLUME   | num     |   444 | DA DECIDERE
#     VENTRALDC_SUVR           | num     |   300 | DA DECIDERE
#     VENTRALDC_VOLUME         | num     |   420 | DA DECIDERE
#     VESSEL_SUVR              | num     |   339 | DA DECIDERE
#     VESSEL_VOLUME            | num     |   137 | DA DECIDERE
#     CTX_LH_BANKSSTS_SUVR     | num     |   312 | DA DECIDERE
#     CTX_LH_BANKSSTS_VOLUME   | num     |   392 | DA DECIDERE
#     CTX_LH_CAUDALANTERIORCINGULATE_SUVR | num     |   311 | DA DECIDERE
#     CTX_LH_CAUDALANTERIORCINGULATE_VOLUME | num     |   394 | DA DECIDERE
#     CTX_LH_CAUDALMIDDLEFRONTAL_SUVR | num     |   301 | DA DECIDERE
#     CTX_LH_CAUDALMIDDLEFRONTAL_VOLUME | num     |   435 | DA DECIDERE
#     CTX_LH_CUNEUS_SUVR       | num     |   289 | DA DECIDERE
#     CTX_LH_CUNEUS_VOLUME     | num     |   408 | DA DECIDERE
#     CTX_LH_ENTORHINAL_SUVR   | num     |   345 | DA DECIDERE
#     CTX_LH_ENTORHINAL_VOLUME | num     |   398 | DA DECIDERE
#     CTX_LH_FRONTALPOLE_SUVR  | num     |   320 | DA DECIDERE
#     CTX_LH_FRONTALPOLE_VOLUME | num     |   342 | DA DECIDERE
#     CTX_LH_FUSIFORM_SUVR     | num     |   302 | DA DECIDERE
#     CTX_LH_FUSIFORM_VOLUME   | num     |   437 | DA DECIDERE
#     CTX_LH_INFERIORPARIETAL_SUVR | num     |   312 | DA DECIDERE
#     CTX_LH_INFERIORPARIETAL_VOLUME | num     |   446 | DA DECIDERE
#     CTX_LH_INFERIORTEMPORAL_SUVR | num     |   321 | DA DECIDERE
#     CTX_LH_INFERIORTEMPORAL_VOLUME | num     |   447 | DA DECIDERE
#     CTX_LH_INSULA_SUVR       | num     |   298 | DA DECIDERE
#     CTX_LH_INSULA_VOLUME     | num     |   422 | DA DECIDERE
#     CTX_LH_ISTHMUSCINGULATE_SUVR | num     |   304 | DA DECIDERE
#     CTX_LH_ISTHMUSCINGULATE_VOLUME | num     |   397 | DA DECIDERE
#     CTX_LH_LATERALOCCIPITAL_SUVR | num     |   313 | DA DECIDERE
#     CTX_LH_LATERALOCCIPITAL_VOLUME | num     |   445 | DA DECIDERE
#     CTX_LH_LATERALORBITOFRONTAL_SUVR | num     |   302 | DA DECIDERE
#     CTX_LH_LATERALORBITOFRONTAL_VOLUME | num     |   416 | DA DECIDERE
#     CTX_LH_LINGUAL_SUVR      | num     |   291 | DA DECIDERE
#     CTX_LH_LINGUAL_VOLUME    | num     |   431 | DA DECIDERE
#     CTX_LH_MEDIALORBITOFRONTAL_SUVR | num     |   299 | DA DECIDERE
#     CTX_LH_MEDIALORBITOFRONTAL_VOLUME | num     |   420 | DA DECIDERE
#     CTX_LH_MIDDLETEMPORAL_SUVR | num     |   326 | DA DECIDERE
#     CTX_LH_MIDDLETEMPORAL_VOLUME | num     |   437 | DA DECIDERE
#     CTX_LH_PARACENTRAL_SUVR  | num     |   280 | DA DECIDERE
#     CTX_LH_PARACENTRAL_VOLUME | num     |   392 | DA DECIDERE
#     CTX_LH_PARAHIPPOCAMPAL_SUVR | num     |   312 | DA DECIDERE
#     CTX_LH_PARAHIPPOCAMPAL_VOLUME | num     |   368 | DA DECIDERE
#     CTX_LH_PARSOPERCULARIS_SUVR | num     |   284 | DA DECIDERE
#     CTX_LH_PARSOPERCULARIS_VOLUME | num     |   418 | DA DECIDERE
#     CTX_LH_PARSORBITALIS_SUVR | num     |   297 | DA DECIDERE
#     CTX_LH_PARSORBITALIS_VOLUME | num     |   383 | DA DECIDERE
#     CTX_LH_PARSTRIANGULARIS_SUVR | num     |   290 | DA DECIDERE
#     CTX_LH_PARSTRIANGULARIS_VOLUME | num     |   409 | DA DECIDERE
#     CTX_LH_PERICALCARINE_SUVR | num     |   284 | DA DECIDERE
#     CTX_LH_PERICALCARINE_VOLUME | num     |   396 | DA DECIDERE
#     CTX_LH_POSTCENTRAL_SUVR  | num     |   268 | DA DECIDERE
#     CTX_LH_POSTCENTRAL_VOLUME | num     |   441 | DA DECIDERE
#     CTX_LH_POSTERIORCINGULATE_SUVR | num     |   315 | DA DECIDERE
#     CTX_LH_POSTERIORCINGULATE_VOLUME | num     |   395 | DA DECIDERE
#     CTX_LH_PRECENTRAL_SUVR   | num     |   264 | DA DECIDERE
#     CTX_LH_PRECENTRAL_VOLUME | num     |   441 | DA DECIDERE
#     CTX_LH_PRECUNEUS_SUVR    | num     |   296 | DA DECIDERE
#     CTX_LH_PRECUNEUS_VOLUME  | num     |   440 | DA DECIDERE
#     CTX_LH_ROSTRALANTERIORCINGULATE_SUVR | num     |   298 | DA DECIDERE
#     CTX_LH_ROSTRALANTERIORCINGULATE_VOLUME | num     |   402 | DA DECIDERE
#     CTX_LH_ROSTRALMIDDLEFRONTAL_SUVR | num     |   278 | DA DECIDERE
#     CTX_LH_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   450 | DA DECIDERE
#     CTX_LH_SUPERIORFRONTAL_SUVR | num     |   290 | DA DECIDERE
#     CTX_LH_SUPERIORFRONTAL_VOLUME | num     |   452 | DA DECIDERE
#     CTX_LH_SUPERIORPARIETAL_SUVR | num     |   299 | DA DECIDERE
#     CTX_LH_SUPERIORPARIETAL_VOLUME | num     |   438 | DA DECIDERE
#     CTX_LH_SUPERIORTEMPORAL_SUVR | num     |   301 | DA DECIDERE
#     CTX_LH_SUPERIORTEMPORAL_VOLUME | num     |   444 | DA DECIDERE
#     CTX_LH_SUPRAMARGINAL_SUVR | num     |   302 | DA DECIDERE
#     CTX_LH_SUPRAMARGINAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_LH_TEMPORALPOLE_SUVR | num     |   322 | DA DECIDERE
#     CTX_LH_TEMPORALPOLE_VOLUME | num     |   413 | DA DECIDERE
#     CTX_LH_TRANSVERSETEMPORAL_SUVR | num     |   297 | DA DECIDERE
#     CTX_LH_TRANSVERSETEMPORAL_VOLUME | num     |   336 | DA DECIDERE
#     CTX_RH_BANKSSTS_SUVR     | num     |   325 | DA DECIDERE
#     CTX_RH_BANKSSTS_VOLUME   | num     |   366 | DA DECIDERE
#     CTX_RH_CAUDALANTERIORCINGULATE_SUVR | num     |   299 | DA DECIDERE
#     CTX_RH_CAUDALANTERIORCINGULATE_VOLUME | num     |   389 | DA DECIDERE
#     CTX_RH_CAUDALMIDDLEFRONTAL_SUVR | num     |   292 | DA DECIDERE
#     CTX_RH_CAUDALMIDDLEFRONTAL_VOLUME | num     |   425 | DA DECIDERE
#     CTX_RH_CUNEUS_SUVR       | num     |   284 | DA DECIDERE
#     CTX_RH_CUNEUS_VOLUME     | num     |   424 | DA DECIDERE
#     CTX_RH_ENTORHINAL_SUVR   | num     |   347 | DA DECIDERE
#     CTX_RH_ENTORHINAL_VOLUME | num     |   396 | DA DECIDERE
#     CTX_RH_FRONTALPOLE_SUVR  | num     |   321 | DA DECIDERE
#     CTX_RH_FRONTALPOLE_VOLUME | num     |   343 | DA DECIDERE
#     CTX_RH_FUSIFORM_SUVR     | num     |   313 | DA DECIDERE
#     CTX_RH_FUSIFORM_VOLUME   | num     |   430 | DA DECIDERE
#     CTX_RH_INFERIORPARIETAL_SUVR | num     |   312 | DA DECIDERE
#     CTX_RH_INFERIORPARIETAL_VOLUME | num     |   451 | DA DECIDERE
#     CTX_RH_INFERIORTEMPORAL_SUVR | num     |   325 | DA DECIDERE
#     CTX_RH_INFERIORTEMPORAL_VOLUME | num     |   435 | DA DECIDERE
#     CTX_RH_INSULA_SUVR       | num     |   301 | DA DECIDERE
#     CTX_RH_INSULA_VOLUME     | num     |   423 | DA DECIDERE
#     CTX_RH_ISTHMUSCINGULATE_SUVR | num     |   306 | DA DECIDERE
#     CTX_RH_ISTHMUSCINGULATE_VOLUME | num     |   382 | DA DECIDERE
#     CTX_RH_LATERALOCCIPITAL_SUVR | num     |   321 | DA DECIDERE
#     CTX_RH_LATERALOCCIPITAL_VOLUME | num     |   444 | DA DECIDERE
#     CTX_RH_LATERALORBITOFRONTAL_SUVR | num     |   308 | DA DECIDERE
#     CTX_RH_LATERALORBITOFRONTAL_VOLUME | num     |   412 | DA DECIDERE
#     CTX_RH_LINGUAL_SUVR      | num     |   283 | DA DECIDERE
#     CTX_RH_LINGUAL_VOLUME    | num     |   436 | DA DECIDERE
#     CTX_RH_MEDIALORBITOFRONTAL_SUVR | num     |   306 | DA DECIDERE
#     CTX_RH_MEDIALORBITOFRONTAL_VOLUME | num     |   419 | DA DECIDERE
#     CTX_RH_MIDDLETEMPORAL_SUVR | num     |   315 | DA DECIDERE
#     CTX_RH_MIDDLETEMPORAL_VOLUME | num     |   434 | DA DECIDERE
#     CTX_RH_PARACENTRAL_SUVR  | num     |   274 | DA DECIDERE
#     CTX_RH_PARACENTRAL_VOLUME | num     |   406 | DA DECIDERE
#     CTX_RH_PARAHIPPOCAMPAL_SUVR | num     |   312 | DA DECIDERE
#     CTX_RH_PARAHIPPOCAMPAL_VOLUME | num     |   365 | DA DECIDERE
#     CTX_RH_PARSOPERCULARIS_SUVR | num     |   298 | DA DECIDERE
#     CTX_RH_PARSOPERCULARIS_VOLUME | num     |   414 | DA DECIDERE
#     CTX_RH_PARSORBITALIS_SUVR | num     |   295 | DA DECIDERE
#     CTX_RH_PARSORBITALIS_VOLUME | num     |   373 | DA DECIDERE
#     CTX_RH_PARSTRIANGULARIS_SUVR | num     |   307 | DA DECIDERE
#     CTX_RH_PARSTRIANGULARIS_VOLUME | num     |   416 | DA DECIDERE
#     CTX_RH_PERICALCARINE_SUVR | num     |   271 | DA DECIDERE
#     CTX_RH_PERICALCARINE_VOLUME | num     |   410 | DA DECIDERE
#     CTX_RH_POSTCENTRAL_SUVR  | num     |   271 | DA DECIDERE
#     CTX_RH_POSTCENTRAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_RH_POSTERIORCINGULATE_SUVR | num     |   310 | DA DECIDERE
#     CTX_RH_POSTERIORCINGULATE_VOLUME | num     |   403 | DA DECIDERE
#     CTX_RH_PRECENTRAL_SUVR   | num     |   259 | DA DECIDERE
#     CTX_RH_PRECENTRAL_VOLUME | num     |   433 | DA DECIDERE
#     CTX_RH_PRECUNEUS_SUVR    | num     |   296 | DA DECIDERE
#     CTX_RH_PRECUNEUS_VOLUME  | num     |   436 | DA DECIDERE
#     CTX_RH_ROSTRALANTERIORCINGULATE_SUVR | num     |   310 | DA DECIDERE
#     CTX_RH_ROSTRALANTERIORCINGULATE_VOLUME | num     |   392 | DA DECIDERE
#     CTX_RH_ROSTRALMIDDLEFRONTAL_SUVR | num     |   287 | DA DECIDERE
#     CTX_RH_ROSTRALMIDDLEFRONTAL_VOLUME | num     |   448 | DA DECIDERE
#     CTX_RH_SUPERIORFRONTAL_SUVR | num     |   284 | DA DECIDERE
#     CTX_RH_SUPERIORFRONTAL_VOLUME | num     |   447 | DA DECIDERE
#     CTX_RH_SUPERIORPARIETAL_SUVR | num     |   301 | DA DECIDERE
#     CTX_RH_SUPERIORPARIETAL_VOLUME | num     |   439 | DA DECIDERE
#     CTX_RH_SUPERIORTEMPORAL_SUVR | num     |   305 | DA DECIDERE
#     CTX_RH_SUPERIORTEMPORAL_VOLUME | num     |   442 | DA DECIDERE
#     CTX_RH_SUPRAMARGINAL_SUVR | num     |   291 | DA DECIDERE
#     CTX_RH_SUPRAMARGINAL_VOLUME | num     |   440 | DA DECIDERE
#     CTX_RH_TEMPORALPOLE_SUVR | num     |   334 | DA DECIDERE
#     CTX_RH_TEMPORALPOLE_VOLUME | num     |   399 | DA DECIDERE
#     CTX_RH_TRANSVERSETEMPORAL_SUVR | num     |   296 | DA DECIDERE
#     CTX_RH_TRANSVERSETEMPORAL_VOLUME | num     |   312 | DA DECIDERE
#     LEFT_ACCUMBENS_AREA_SUVR | num     |   347 | DA DECIDERE
#     LEFT_ACCUMBENS_AREA_VOLUME | num     |   243 | DA DECIDERE
#     LEFT_AMYGDALA_SUVR       | num     |   353 | DA DECIDERE
#     LEFT_AMYGDALA_VOLUME     | num     |   364 | DA DECIDERE
#     LEFT_CAUDATE_SUVR        | num     |   327 | DA DECIDERE
#     LEFT_CAUDATE_VOLUME      | num     |   410 | DA DECIDERE
#     LEFT_CEREBELLUM_CORTEX_SUVR | num     |   111 | DA DECIDERE
#     LEFT_CEREBELLUM_CORTEX_VOLUME | num     |   456 | DA DECIDERE
#     LEFT_CEREBELLUM_WHITE_MATTER_SUVR | num     |   232 | DA DECIDERE
#     LEFT_CEREBELLUM_WHITE_MATTER_VOLUME | num     |   450 | DA DECIDERE
#     LEFT_CEREBRAL_WHITE_MATTER_SUVR | num     |   305 | DA DECIDERE
#     LEFT_CEREBRAL_WHITE_MATTER_VOLUME | num     |   462 | DA DECIDERE
#     LEFT_CHOROID_PLEXUS_SUVR | num     |   407 | DA DECIDERE
#     LEFT_CHOROID_PLEXUS_VOLUME | num     |   348 | DA DECIDERE
#     LEFT_HIPPOCAMPUS_SUVR    | num     |   337 | DA DECIDERE
#     LEFT_HIPPOCAMPUS_VOLUME  | num     |   413 | DA DECIDERE
#     LEFT_INF_LAT_VENT_SUVR   | num     |   361 | DA DECIDERE
#     LEFT_INF_LAT_VENT_VOLUME | num     |   403 | DA DECIDERE
#     LEFT_LATERAL_VENTRICLE_SUVR | num     |   341 | DA DECIDERE
#     LEFT_LATERAL_VENTRICLE_VOLUME | num     |   462 | DA DECIDERE
#     LEFT_PALLIDUM_SUVR       | num     |   360 | DA DECIDERE
#     LEFT_PALLIDUM_VOLUME     | num     |   357 | DA DECIDERE
#     LEFT_PUTAMEN_SUVR        | num     |   364 | DA DECIDERE
#     LEFT_PUTAMEN_VOLUME      | num     |   420 | DA DECIDERE
#     LEFT_THALAMUS_PROPER_SUVR | num     |   281 | DA DECIDERE
#     LEFT_THALAMUS_PROPER_VOLUME | num     |   422 | DA DECIDERE
#     LEFT_VENTRALDC_SUVR      | num     |   306 | DA DECIDERE
#     LEFT_VENTRALDC_VOLUME    | num     |   401 | DA DECIDERE
#     LEFT_VESSEL_SUVR         | num     |   345 | DA DECIDERE
#     LEFT_VESSEL_VOLUME       | num     |    98 | DA DECIDERE
#     RIGHT_ACCUMBENS_AREA_SUVR | num     |   341 | DA DECIDERE
#     RIGHT_ACCUMBENS_AREA_VOLUME | num     |   256 | DA DECIDERE
#     RIGHT_AMYGDALA_SUVR      | num     |   359 | DA DECIDERE
#     RIGHT_AMYGDALA_VOLUME    | num     |   372 | DA DECIDERE
#     RIGHT_CAUDATE_SUVR       | num     |   329 | DA DECIDERE
#     RIGHT_CAUDATE_VOLUME     | num     |   403 | DA DECIDERE
#     RIGHT_CEREBELLUM_CORTEX_SUVR | num     |   114 | DA DECIDERE
#     RIGHT_CEREBELLUM_CORTEX_VOLUME | num     |   459 | DA DECIDERE
#     RIGHT_CEREBELLUM_WHITE_MATTER_SUVR | num     |   248 | DA DECIDERE
#     RIGHT_CEREBELLUM_WHITE_MATTER_VOLUME | num     |   441 | DA DECIDERE
#     RIGHT_CEREBRAL_WHITE_MATTER_SUVR | num     |   312 | DA DECIDERE
#     RIGHT_CEREBRAL_WHITE_MATTER_VOLUME | num     |   460 | DA DECIDERE
#     RIGHT_CHOROID_PLEXUS_SUVR | num     |   401 | DA DECIDERE
#     RIGHT_CHOROID_PLEXUS_VOLUME | num     |   353 | DA DECIDERE
#     RIGHT_HIPPOCAMPUS_SUVR   | num     |   343 | DA DECIDERE
#     RIGHT_HIPPOCAMPUS_VOLUME | num     |   413 | DA DECIDERE
#     RIGHT_INF_LAT_VENT_SUVR  | num     |   367 | DA DECIDERE
#     RIGHT_INF_LAT_VENT_VOLUME | num     |   397 | DA DECIDERE
#     RIGHT_LATERAL_VENTRICLE_SUVR | num     |   327 | DA DECIDERE
#     RIGHT_LATERAL_VENTRICLE_VOLUME | num     |   458 | DA DECIDERE
#     RIGHT_PALLIDUM_SUVR      | num     |   350 | DA DECIDERE
#     RIGHT_PALLIDUM_VOLUME    | num     |   371 | DA DECIDERE
#     RIGHT_PUTAMEN_SUVR       | num     |   350 | DA DECIDERE
#     RIGHT_PUTAMEN_VOLUME     | num     |   419 | DA DECIDERE
#     RIGHT_THALAMUS_PROPER_SUVR | num     |   300 | DA DECIDERE
#     RIGHT_THALAMUS_PROPER_VOLUME | num     |   420 | DA DECIDERE
#     RIGHT_VENTRALDC_SUVR     | num     |   307 | DA DECIDERE
#     RIGHT_VENTRALDC_VOLUME   | num     |   401 | DA DECIDERE
#     RIGHT_VESSEL_SUVR        | num     |   339 | DA DECIDERE
#     RIGHT_VESSEL_VOLUME      | num     |    89 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UCBERKELEY_TAU_6MM = DatasetConfig(
    file_code="UCBERKELEY_TAU_6MM",                          # <-- VERIFICA
    source="UCBERKELEY_TAU_6MM_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['pet'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="SCANDATE",          # preferenza ADNI (alt: ['PROCESSDATE', 'update_stamp']) VERIFICA
    # 329 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['IMAGE_RESOLUTION', 'TRACER', 'TRACER_SUVR_WARNING', 'META_TEMPORAL_SUVR', 'META_TEMPORAL_VOLUME', 'CTX_ENTORHINAL_SUVR', 'CTX_ENTORHINAL_VOLUME', 'INFERIORCEREBELLUM_SUVR', 'INFERIORCEREBELLUM_VOLUME', 'ERODED_SUBCORTICALWM_SUVR', 'ERODED_SUBCORTICALWM_VOLUME', 'BRAINSTEM_SUVR', 'BRAINSTEM_VOLUME', 'CC_ANTERIOR_SUVR', 'CC_ANTERIOR_VOLUME', 'CC_CENTRAL_SUVR', 'CC_CENTRAL_VOLUME', 'CC_MID_ANTERIOR_SUVR', 'CC_MID_ANTERIOR_VOLUME', 'CC_MID_POSTERIOR_SUVR', 'CC_MID_POSTERIOR_VOLUME', 'CC_POSTERIOR_SUVR', 'CC_POSTERIOR_VOLUME', 'CSF_SUVR', 'CSF_VOLUME', 'VENTRICLE_3RD_SUVR', 'VENTRICLE_3RD_VOLUME', 'VENTRICLE_4TH_SUVR', 'VENTRICLE_4TH_VOLUME', 'VENTRICLE_5TH_SUVR', 'VENTRICLE_5TH_VOLUME', 'WM_HYPOINTENSITIES_SUVR', 'WM_HYPOINTENSITIES_VOLUME', 'NON_WM_HYPOINTENSITIES_SUVR', 'NON_WM_HYPOINTENSITIES_VOLUME', 'CTX_BANKSSTS_SUVR', 'CTX_BANKSSTS_VOLUME', 'CTX_CAUDALANTERIORCINGULATE_SUVR', 'CTX_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_CUNEUS_SUVR', 'CTX_CUNEUS_VOLUME', 'CTX_FRONTALPOLE_SUVR', 'CTX_FRONTALPOLE_VOLUME', 'CTX_FUSIFORM_SUVR', 'CTX_FUSIFORM_VOLUME', 'CTX_INFERIORPARIETAL_SUVR', 'CTX_INFERIORPARIETAL_VOLUME', 'CTX_INFERIORTEMPORAL_SUVR', 'CTX_INFERIORTEMPORAL_VOLUME', 'CTX_INSULA_SUVR', 'CTX_INSULA_VOLUME', 'CTX_ISTHMUSCINGULATE_SUVR', 'CTX_ISTHMUSCINGULATE_VOLUME', 'CTX_LATERALOCCIPITAL_SUVR', 'CTX_LATERALOCCIPITAL_VOLUME', 'CTX_LATERALORBITOFRONTAL_SUVR', 'CTX_LATERALORBITOFRONTAL_VOLUME', 'CTX_LINGUAL_SUVR', 'CTX_LINGUAL_VOLUME', 'CTX_MEDIALORBITOFRONTAL_SUVR', 'CTX_MEDIALORBITOFRONTAL_VOLUME', 'CTX_MIDDLETEMPORAL_SUVR', 'CTX_MIDDLETEMPORAL_VOLUME', 'CTX_PARACENTRAL_SUVR', 'CTX_PARACENTRAL_VOLUME', 'CTX_PARAHIPPOCAMPAL_SUVR', 'CTX_PARAHIPPOCAMPAL_VOLUME', 'CTX_PARSOPERCULARIS_SUVR', 'CTX_PARSOPERCULARIS_VOLUME', 'CTX_PARSORBITALIS_SUVR', 'CTX_PARSORBITALIS_VOLUME', 'CTX_PARSTRIANGULARIS_SUVR', 'CTX_PARSTRIANGULARIS_VOLUME', 'CTX_PERICALCARINE_SUVR', 'CTX_PERICALCARINE_VOLUME', 'CTX_POSTCENTRAL_SUVR', 'CTX_POSTCENTRAL_VOLUME', 'CTX_POSTERIORCINGULATE_SUVR', 'CTX_POSTERIORCINGULATE_VOLUME', 'CTX_PRECENTRAL_SUVR', 'CTX_PRECENTRAL_VOLUME', 'CTX_PRECUNEUS_SUVR', 'CTX_PRECUNEUS_VOLUME', 'CTX_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_SUPERIORFRONTAL_SUVR', 'CTX_SUPERIORFRONTAL_VOLUME', 'CTX_SUPERIORPARIETAL_SUVR', 'CTX_SUPERIORPARIETAL_VOLUME', 'CTX_SUPERIORTEMPORAL_SUVR', 'CTX_SUPERIORTEMPORAL_VOLUME', 'CTX_SUPRAMARGINAL_SUVR', 'CTX_SUPRAMARGINAL_VOLUME', 'CTX_TEMPORALPOLE_SUVR', 'CTX_TEMPORALPOLE_VOLUME', 'CTX_TRANSVERSETEMPORAL_SUVR', 'CTX_TRANSVERSETEMPORAL_VOLUME', 'ACCUMBENS_AREA_SUVR', 'ACCUMBENS_AREA_VOLUME', 'AMYGDALA_SUVR', 'AMYGDALA_VOLUME', 'CAUDATE_SUVR', 'CAUDATE_VOLUME', 'CEREBELLUM_CORTEX_SUVR', 'CEREBELLUM_CORTEX_VOLUME', 'CEREBELLUM_WHITE_MATTER_SUVR', 'CEREBELLUM_WHITE_MATTER_VOLUME', 'CEREBRAL_WHITE_MATTER_SUVR', 'CEREBRAL_WHITE_MATTER_VOLUME', 'CHOROID_PLEXUS_SUVR', 'CHOROID_PLEXUS_VOLUME', 'HIPPOCAMPUS_SUVR', 'HIPPOCAMPUS_VOLUME', 'OPTIC_CHIASM_SUVR', 'OPTIC_CHIASM_VOLUME', 'INF_LAT_VENT_SUVR', 'INF_LAT_VENT_VOLUME', 'LATERAL_VENTRICLE_SUVR', 'LATERAL_VENTRICLE_VOLUME', 'PALLIDUM_SUVR', 'PALLIDUM_VOLUME', 'PUTAMEN_SUVR', 'PUTAMEN_VOLUME', 'THALAMUS_PROPER_SUVR', 'THALAMUS_PROPER_VOLUME', 'VENTRALDC_SUVR', 'VENTRALDC_VOLUME', 'VESSEL_SUVR', 'VESSEL_VOLUME', 'CTX_LH_BANKSSTS_SUVR', 'CTX_LH_BANKSSTS_VOLUME', 'CTX_LH_CAUDALANTERIORCINGULATE_SUVR', 'CTX_LH_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_LH_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_LH_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_LH_CUNEUS_SUVR', 'CTX_LH_CUNEUS_VOLUME', 'CTX_LH_ENTORHINAL_SUVR', 'CTX_LH_ENTORHINAL_VOLUME', 'CTX_LH_FRONTALPOLE_SUVR', 'CTX_LH_FRONTALPOLE_VOLUME', 'CTX_LH_FUSIFORM_SUVR', 'CTX_LH_FUSIFORM_VOLUME', 'CTX_LH_INFERIORPARIETAL_SUVR', 'CTX_LH_INFERIORPARIETAL_VOLUME', 'CTX_LH_INFERIORTEMPORAL_SUVR', 'CTX_LH_INFERIORTEMPORAL_VOLUME', 'CTX_LH_INSULA_SUVR', 'CTX_LH_INSULA_VOLUME', 'CTX_LH_ISTHMUSCINGULATE_SUVR', 'CTX_LH_ISTHMUSCINGULATE_VOLUME', 'CTX_LH_LATERALOCCIPITAL_SUVR', 'CTX_LH_LATERALOCCIPITAL_VOLUME', 'CTX_LH_LATERALORBITOFRONTAL_SUVR', 'CTX_LH_LATERALORBITOFRONTAL_VOLUME', 'CTX_LH_LINGUAL_SUVR', 'CTX_LH_LINGUAL_VOLUME', 'CTX_LH_MEDIALORBITOFRONTAL_SUVR', 'CTX_LH_MEDIALORBITOFRONTAL_VOLUME', 'CTX_LH_MIDDLETEMPORAL_SUVR', 'CTX_LH_MIDDLETEMPORAL_VOLUME', 'CTX_LH_PARACENTRAL_SUVR', 'CTX_LH_PARACENTRAL_VOLUME', 'CTX_LH_PARAHIPPOCAMPAL_SUVR', 'CTX_LH_PARAHIPPOCAMPAL_VOLUME', 'CTX_LH_PARSOPERCULARIS_SUVR', 'CTX_LH_PARSOPERCULARIS_VOLUME', 'CTX_LH_PARSORBITALIS_SUVR', 'CTX_LH_PARSORBITALIS_VOLUME', 'CTX_LH_PARSTRIANGULARIS_SUVR', 'CTX_LH_PARSTRIANGULARIS_VOLUME', 'CTX_LH_PERICALCARINE_SUVR', 'CTX_LH_PERICALCARINE_VOLUME', 'CTX_LH_POSTCENTRAL_SUVR', 'CTX_LH_POSTCENTRAL_VOLUME', 'CTX_LH_POSTERIORCINGULATE_SUVR', 'CTX_LH_POSTERIORCINGULATE_VOLUME', 'CTX_LH_PRECENTRAL_SUVR', 'CTX_LH_PRECENTRAL_VOLUME', 'CTX_LH_PRECUNEUS_SUVR', 'CTX_LH_PRECUNEUS_VOLUME', 'CTX_LH_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_LH_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_LH_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_LH_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_LH_SUPERIORFRONTAL_SUVR', 'CTX_LH_SUPERIORFRONTAL_VOLUME', 'CTX_LH_SUPERIORPARIETAL_SUVR', 'CTX_LH_SUPERIORPARIETAL_VOLUME', 'CTX_LH_SUPERIORTEMPORAL_SUVR', 'CTX_LH_SUPERIORTEMPORAL_VOLUME', 'CTX_LH_SUPRAMARGINAL_SUVR', 'CTX_LH_SUPRAMARGINAL_VOLUME', 'CTX_LH_TEMPORALPOLE_SUVR', 'CTX_LH_TEMPORALPOLE_VOLUME', 'CTX_LH_TRANSVERSETEMPORAL_SUVR', 'CTX_LH_TRANSVERSETEMPORAL_VOLUME', 'CTX_RH_BANKSSTS_SUVR', 'CTX_RH_BANKSSTS_VOLUME', 'CTX_RH_CAUDALANTERIORCINGULATE_SUVR', 'CTX_RH_CAUDALANTERIORCINGULATE_VOLUME', 'CTX_RH_CAUDALMIDDLEFRONTAL_SUVR', 'CTX_RH_CAUDALMIDDLEFRONTAL_VOLUME', 'CTX_RH_CUNEUS_SUVR', 'CTX_RH_CUNEUS_VOLUME', 'CTX_RH_ENTORHINAL_SUVR', 'CTX_RH_ENTORHINAL_VOLUME', 'CTX_RH_FRONTALPOLE_SUVR', 'CTX_RH_FRONTALPOLE_VOLUME', 'CTX_RH_FUSIFORM_SUVR', 'CTX_RH_FUSIFORM_VOLUME', 'CTX_RH_INFERIORPARIETAL_SUVR', 'CTX_RH_INFERIORPARIETAL_VOLUME', 'CTX_RH_INFERIORTEMPORAL_SUVR', 'CTX_RH_INFERIORTEMPORAL_VOLUME', 'CTX_RH_INSULA_SUVR', 'CTX_RH_INSULA_VOLUME', 'CTX_RH_ISTHMUSCINGULATE_SUVR', 'CTX_RH_ISTHMUSCINGULATE_VOLUME', 'CTX_RH_LATERALOCCIPITAL_SUVR', 'CTX_RH_LATERALOCCIPITAL_VOLUME', 'CTX_RH_LATERALORBITOFRONTAL_SUVR', 'CTX_RH_LATERALORBITOFRONTAL_VOLUME', 'CTX_RH_LINGUAL_SUVR', 'CTX_RH_LINGUAL_VOLUME', 'CTX_RH_MEDIALORBITOFRONTAL_SUVR', 'CTX_RH_MEDIALORBITOFRONTAL_VOLUME', 'CTX_RH_MIDDLETEMPORAL_SUVR', 'CTX_RH_MIDDLETEMPORAL_VOLUME', 'CTX_RH_PARACENTRAL_SUVR', 'CTX_RH_PARACENTRAL_VOLUME', 'CTX_RH_PARAHIPPOCAMPAL_SUVR', 'CTX_RH_PARAHIPPOCAMPAL_VOLUME', 'CTX_RH_PARSOPERCULARIS_SUVR', 'CTX_RH_PARSOPERCULARIS_VOLUME', 'CTX_RH_PARSORBITALIS_SUVR', 'CTX_RH_PARSORBITALIS_VOLUME', 'CTX_RH_PARSTRIANGULARIS_SUVR', 'CTX_RH_PARSTRIANGULARIS_VOLUME', 'CTX_RH_PERICALCARINE_SUVR', 'CTX_RH_PERICALCARINE_VOLUME', 'CTX_RH_POSTCENTRAL_SUVR', 'CTX_RH_POSTCENTRAL_VOLUME', 'CTX_RH_POSTERIORCINGULATE_SUVR', 'CTX_RH_POSTERIORCINGULATE_VOLUME', 'CTX_RH_PRECENTRAL_SUVR', 'CTX_RH_PRECENTRAL_VOLUME', 'CTX_RH_PRECUNEUS_SUVR', 'CTX_RH_PRECUNEUS_VOLUME', 'CTX_RH_ROSTRALANTERIORCINGULATE_SUVR', 'CTX_RH_ROSTRALANTERIORCINGULATE_VOLUME', 'CTX_RH_ROSTRALMIDDLEFRONTAL_SUVR', 'CTX_RH_ROSTRALMIDDLEFRONTAL_VOLUME', 'CTX_RH_SUPERIORFRONTAL_SUVR', 'CTX_RH_SUPERIORFRONTAL_VOLUME', 'CTX_RH_SUPERIORPARIETAL_SUVR', 'CTX_RH_SUPERIORPARIETAL_VOLUME', 'CTX_RH_SUPERIORTEMPORAL_SUVR', 'CTX_RH_SUPERIORTEMPORAL_VOLUME', 'CTX_RH_SUPRAMARGINAL_SUVR', 'CTX_RH_SUPRAMARGINAL_VOLUME', 'CTX_RH_TEMPORALPOLE_SUVR', 'CTX_RH_TEMPORALPOLE_VOLUME', 'CTX_RH_TRANSVERSETEMPORAL_SUVR', 'CTX_RH_TRANSVERSETEMPORAL_VOLUME', 'LEFT_ACCUMBENS_AREA_SUVR', 'LEFT_ACCUMBENS_AREA_VOLUME', 'LEFT_AMYGDALA_SUVR', 'LEFT_AMYGDALA_VOLUME', 'LEFT_CAUDATE_SUVR', 'LEFT_CAUDATE_VOLUME', 'LEFT_CEREBELLUM_CORTEX_SUVR', 'LEFT_CEREBELLUM_CORTEX_VOLUME', 'LEFT_CEREBELLUM_WHITE_MATTER_SUVR', 'LEFT_CEREBELLUM_WHITE_MATTER_VOLUME', 'LEFT_CEREBRAL_WHITE_MATTER_SUVR', 'LEFT_CEREBRAL_WHITE_MATTER_VOLUME', 'LEFT_CHOROID_PLEXUS_SUVR', 'LEFT_CHOROID_PLEXUS_VOLUME', 'LEFT_HIPPOCAMPUS_SUVR', 'LEFT_HIPPOCAMPUS_VOLUME', 'LEFT_INF_LAT_VENT_SUVR', 'LEFT_INF_LAT_VENT_VOLUME', 'LEFT_LATERAL_VENTRICLE_SUVR', 'LEFT_LATERAL_VENTRICLE_VOLUME', 'LEFT_PALLIDUM_SUVR', 'LEFT_PALLIDUM_VOLUME', 'LEFT_PUTAMEN_SUVR', 'LEFT_PUTAMEN_VOLUME', 'LEFT_THALAMUS_PROPER_SUVR', 'LEFT_THALAMUS_PROPER_VOLUME', 'LEFT_VENTRALDC_SUVR', 'LEFT_VENTRALDC_VOLUME', 'LEFT_VESSEL_SUVR', 'LEFT_VESSEL_VOLUME', 'RIGHT_ACCUMBENS_AREA_SUVR', 'RIGHT_ACCUMBENS_AREA_VOLUME', 'RIGHT_AMYGDALA_SUVR', 'RIGHT_AMYGDALA_VOLUME', 'RIGHT_CAUDATE_SUVR', 'RIGHT_CAUDATE_VOLUME', 'RIGHT_CEREBELLUM_CORTEX_SUVR', 'RIGHT_CEREBELLUM_CORTEX_VOLUME', 'RIGHT_CEREBELLUM_WHITE_MATTER_SUVR', 'RIGHT_CEREBELLUM_WHITE_MATTER_VOLUME', 'RIGHT_CEREBRAL_WHITE_MATTER_SUVR', 'RIGHT_CEREBRAL_WHITE_MATTER_VOLUME', 'RIGHT_CHOROID_PLEXUS_SUVR', 'RIGHT_CHOROID_PLEXUS_VOLUME', 'RIGHT_HIPPOCAMPUS_SUVR', 'RIGHT_HIPPOCAMPUS_VOLUME', 'RIGHT_INF_LAT_VENT_SUVR', 'RIGHT_INF_LAT_VENT_VOLUME', 'RIGHT_LATERAL_VENTRICLE_SUVR', 'RIGHT_LATERAL_VENTRICLE_VOLUME', 'RIGHT_PALLIDUM_SUVR', 'RIGHT_PALLIDUM_VOLUME', 'RIGHT_PUTAMEN_SUVR', 'RIGHT_PUTAMEN_VOLUME', 'RIGHT_THALAMUS_PROPER_SUVR', 'RIGHT_THALAMUS_PROPER_VOLUME', 'RIGHT_VENTRALDC_SUVR', 'RIGHT_VENTRALDC_VOLUME', 'RIGHT_VESSEL_SUVR', 'RIGHT_VESSEL_VOLUME']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCD_ADNI1_WMH
#   source: UCD_ADNI1_WMH_11Aug2025.csv   |   righe campionate: 500   |   colonne: 10
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   109 | cand. ID
#     EXAMDATE                 | date    |   371 | cand. DATA
#     VISCODE                  | cat/str |     8 | cand. VISITA
#     WHITMATHYP               | num     |   500 | DA DECIDERE
#     MANUFACTURER             | cat/str |     3 | DA DECIDERE
#     MODEL                    | cat/str |    14 | DA DECIDERE
#     MAGSTRENGTH              | num     |     1 | DA DECIDERE
#     SEGPROCIMG               | cat/str |     1 | DA DECIDERE
#     SEGPROC                  | cat/str |     1 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UCD_ADNI1_WMH = DatasetConfig(
    file_code="UCD_ADNI1_WMH",                          # <-- VERIFICA
    source="UCD_ADNI1_WMH_11Aug2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 6 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['WHITMATHYP', 'MANUFACTURER', 'MODEL', 'MAGSTRENGTH', 'SEGPROCIMG', 'SEGPROC']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCD_WMH
#   source: UCD_WMH_11Aug2025.csv   |   righe campionate: 500   |   colonne: 27
#   ignorate 3 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   148 | cand. ID
#     RID                      | num     |   148 | cand. ID
#     VISCODE                  | cat/str |    21 | cand. VISITA
#     VISCODE2                 | cat/str |    27 | cand. VISITA
#     EXAMDATE                 | date    |   433 | cand. DATA
#     RUNDATE                  | date    |     1 | cand. DATA
#     MANUFACTURER             | cat/str |     4 | DA DECIDERE
#     MANUFACTURERSMODELNAME   | cat/str |     7 | DA DECIDERE
#     MAGNETICFIELDSTRENGTH    | num     |     1 | DA DECIDERE
#     MRACQUISITIONTYPEFLAIR   | cat/str |     2 | DA DECIDERE
#     CEREBRUM_TCV             | num     |   498 | DA DECIDERE
#     CEREBRUM_TCB             | num     |   499 | DA DECIDERE
#     CEREBRUM_TCC             | num     |   498 | DA DECIDERE
#     CEREBRUM_GRAY            | num     |   500 | DA DECIDERE
#     CEREBRUM_WHITE           | num     |   499 | DA DECIDERE
#     LEFT_HIPPO               | num     |   474 | DA DECIDERE
#     RIGHT_HIPPO              | num     |   468 | DA DECIDERE
#     TOTAL_HIPPO              | num     |   486 | DA DECIDERE
#     TOTAL_CSF                | num     |   500 | DA DECIDERE
#     TOTAL_GRAY               | num     |   499 | DA DECIDERE
#     TOTAL_WHITE              | num     |   500 | DA DECIDERE
#     TOTAL_WMH                | num     |   496 | DA DECIDERE
#     TOTAL_BRAIN              | num     |   499 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UCD_WMH = DatasetConfig(
    file_code="UCD_WMH",                          # <-- VERIFICA
    source="UCD_WMH_11Aug2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    # 17 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['MANUFACTURER', 'MANUFACTURERSMODELNAME', 'MAGNETICFIELDSTRENGTH', 'MRACQUISITIONTYPEFLAIR', 'CEREBRUM_TCV', 'CEREBRUM_TCB', 'CEREBRUM_TCC', 'CEREBRUM_GRAY', 'CEREBRUM_WHITE', 'LEFT_HIPPO', 'RIGHT_HIPPO', 'TOTAL_HIPPO', 'TOTAL_CSF', 'TOTAL_GRAY', 'TOTAL_WHITE', 'TOTAL_WMH', 'TOTAL_BRAIN']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSDVOL
#   source: UCSDVOL_28Oct2025.csv   |   righe campionate: 500   |   colonne: 24
#   INDIZIO categoria dal nome (NON deciso): ['volumes']
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   117 | cand. ID
#     VISCODE                  | cat/str |     6 | cand. VISITA
#     USERDATE                 | date    |     1 | cand. DATA
#     EXAMDATE                 | date    |   360 | cand. DATA
#     LONISID                  | num     |   499 | DA DECIDERE
#     CDATE                    | date    |     1 | cand. DATA
#     BRAIN                    | num     |   497 | DA DECIDERE
#     EICV                     | num     |   117 | DA DECIDERE
#     VENTRICLES               | num     |   500 | DA DECIDERE
#     LHIPPOC                  | num     |   500 | DA DECIDERE
#     RHIPPOC                  | num     |   497 | DA DECIDERE
#     LINFLATVEN               | num     |   496 | DA DECIDERE
#     RINFLATVEN               | num     |   496 | DA DECIDERE
#     LMIDTEMP                 | num     |   491 | DA DECIDERE
#     RMIDTEMP                 | num     |   489 | DA DECIDERE
#     LINFTEMP                 | num     |   494 | DA DECIDERE
#     RINFTEMP                 | num     |   493 | DA DECIDERE
#     LFUSIFORM                | num     |   491 | DA DECIDERE
#     RFUSIFORM                | num     |   491 | DA DECIDERE
#     LENTORHIN                | num     |   496 | DA DECIDERE
#     RENTORHIN                | num     |   498 | DA DECIDERE
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
UCSDVOL = DatasetConfig(
    file_code="UCSDVOL",                          # <-- VERIFICA
    source="UCSDVOL_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['USERDATE', 'CDATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 16 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['LONISID', 'BRAIN', 'EICV', 'VENTRICLES', 'LHIPPOC', 'RHIPPOC', 'LINFLATVEN', 'RINFLATVEN', 'LMIDTEMP', 'RMIDTEMP', 'LINFTEMP', 'RINFTEMP', 'LFUSIFORM', 'RFUSIFORM', 'LENTORHIN', 'RENTORHIN']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSL51ALL_08_01_16
#   source: UCSFFSL51ALL_08_01_16_11Aug2025.csv   |   righe campionate: 500   |   colonne: 364
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 14 colonne amministrative/QC (vedi IGNORE_* nello script)
#   341 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST149SV', 'ST28SA', 'ST87SA', 'ST1SV', 'ST2SV'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     COLPROT                  | cat/str |     3 | DA DECIDERE
#     RID                      | num     |   104 | cand. ID
#     VISCODE                  | cat/str |    15 | cand. VISITA
#     VISCODE2                 | cat/str |    14 | cand. VISITA
#     EXAMDATE                 | date    |   397 | cand. DATA
#     VERSION                  | date    |    23 | cand. DATA
#     LONISID                  | num     |   500 | DA DECIDERE
#     RUNDATE                  | date    |    23 | cand. DATA
#     update_stamp             | date    |     4 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSL51ALL_08_01_16 = DatasetConfig(
    file_code="UCSFFSL51ALL_08_01_16",                          # <-- VERIFICA
    source="UCSFFSL51ALL_08_01_16_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'update_stamp']) VERIFICA
    # 2 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['COLPROT', 'LONISID']
    # + 341 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSL51Y1_08_01_16
#   source: UCSFFSL51Y1_08_01_16_11Aug2025.csv   |   righe campionate: 500   |   colonne: 364
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 14 colonne amministrative/QC (vedi IGNORE_* nello script)
#   341 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST149SV', 'ST28SA', 'ST87SA', 'ST1SV', 'ST2SV'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     COLPROT                  | cat/str |     3 | DA DECIDERE
#     RID                      | num     |   135 | cand. ID
#     VISCODE                  | cat/str |    12 | cand. VISITA
#     VISCODE2                 | cat/str |     8 | cand. VISITA
#     EXAMDATE                 | date    |   314 | cand. DATA
#     VERSION                  | date    |    51 | cand. DATA
#     LONISID                  | num     |   500 | DA DECIDERE
#     RUNDATE                  | date    |    51 | cand. DATA
#     update_stamp             | date    |     4 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSL51Y1_08_01_16 = DatasetConfig(
    file_code="UCSFFSL51Y1_08_01_16",                          # <-- VERIFICA
    source="UCSFFSL51Y1_08_01_16_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'update_stamp']) VERIFICA
    # 2 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['COLPROT', 'LONISID']
    # + 341 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSL51_03_01_22
#   source: UCSFFSL51_03_01_22_11Aug2025.csv   |   righe campionate: 500   |   colonne: 364
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 14 colonne amministrative/QC (vedi IGNORE_* nello script)
#   341 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST149SV', 'ST28SA', 'ST87SA', 'ST1SV', 'ST2SV'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     COLPROT                  | cat/str |     2 | DA DECIDERE
#     RID                      | num     |    98 | cand. ID
#     VISCODE                  | cat/str |     7 | cand. VISITA
#     VISCODE2                 | cat/str |    14 | cand. VISITA
#     EXAMDATE                 | date    |   393 | cand. DATA
#     VERSION                  | date    |    21 | cand. DATA
#     LONISID                  | num     |   492 | DA DECIDERE
#     RUNDATE                  | date    |    21 | cand. DATA
#     update_stamp             | date    |     7 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSL51_03_01_22 = DatasetConfig(
    file_code="UCSFFSL51_03_01_22",                          # <-- VERIFICA
    source="UCSFFSL51_03_01_22_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'update_stamp']) VERIFICA
    # 2 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['COLPROT', 'LONISID']
    # + 341 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSL_02_01_16
#   source: UCSFFSL_02_01_16_11Aug2025.csv   |   righe campionate: 500   |   colonne: 375
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 12 colonne amministrative/QC (vedi IGNORE_* nello script)
#   346 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST100SV', 'ST101SV', 'ST102CV', 'ST102SA', 'ST102TA'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   102 | cand. ID
#     VISCODE                  | cat/str |    10 | cand. VISITA
#     VISCODE2                 | cat/str |    10 | cand. VISITA
#     EXAMDATE                 | date    |   373 | cand. DATA
#     VERSION                  | date    |    77 | cand. DATA
#     FLDSTRENG                | num     |     1 | DA DECIDERE
#     LONISID                  | num     |   496 | DA DECIDERE
#     RUNDATE                  | date    |    77 | cand. DATA
#     BASETP1                  | num     |     2 | DA DECIDERE
#     BASETP2                  | num     |     2 | DA DECIDERE
#     BASETP3                  | num     |     2 | DA DECIDERE
#     BASETP4                  | num     |     2 | DA DECIDERE
#     BASETP5                  | num     |     2 | DA DECIDERE
#     BASETP6                  | num     |     2 | DA DECIDERE
#     BASETP7                  | num     |     2 | DA DECIDERE
#     BASETP8                  | num     |     1 | DA DECIDERE
#     update_stamp             | date    |     4 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSL_02_01_16 = DatasetConfig(
    file_code="UCSFFSL_02_01_16",                          # <-- VERIFICA
    source="UCSFFSL_02_01_16_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'update_stamp']) VERIFICA
    # 10 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['FLDSTRENG', 'LONISID', 'BASETP1', 'BASETP2', 'BASETP3', 'BASETP4', 'BASETP5', 'BASETP6', 'BASETP7', 'BASETP8']
    # + 346 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSX51_11_08_19
#   source: UCSFFSX51_11_08_19_11Aug2025.csv   |   righe campionate: 500   |   colonne: 365
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 14 colonne amministrative/QC (vedi IGNORE_* nello script)
#   341 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST101SV', 'ST102CV', 'ST102SA', 'ST102TA', 'ST102TS'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     COLPROT                  | cat/str |     3 | DA DECIDERE
#     RID                      | num     |   122 | cand. ID
#     VISCODE                  | cat/str |     7 | cand. VISITA
#     VISCODE2                 | cat/str |    13 | cand. VISITA
#     EXAMDATE                 | date    |   333 | cand. DATA
#     VERSION                  | date    |   142 | cand. DATA
#     LONISID                  | num     |   367 | DA DECIDERE
#     IMAGETYPE                | cat/str |     2 | DA DECIDERE
#     RUNDATE                  | date    |   142 | cand. DATA
#     update_stamp             | date    |     3 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSX51_11_08_19 = DatasetConfig(
    file_code="UCSFFSX51_11_08_19",                          # <-- VERIFICA
    source="UCSFFSX51_11_08_19_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'update_stamp']) VERIFICA
    # 3 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['COLPROT', 'LONISID', 'IMAGETYPE']
    # + 341 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSX51_ADNI1_3T_02_01_16
#   source: UCSFFSX51_ADNI1_3T_02_01_16_11Aug2025.csv   |   righe campionate: 484   |   colonne: 394
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 14 colonne amministrative/QC (vedi IGNORE_* nello script)
#   373 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST100SV', 'ST101SV', 'ST102CV', 'ST102SA', 'ST102TA'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   143 | cand. ID
#     VISCODE                  | cat/str |     6 | cand. VISITA
#     EXAMDATE                 | date    |   361 | cand. DATA
#     VERSION                  | date    |    38 | cand. DATA
#     LONISID                  | num     |   483 | DA DECIDERE
#     RUNDATE                  | date    |    38 | cand. DATA
#     update_stamp             | date    |     5 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSX51_ADNI1_3T_02_01_16 = DatasetConfig(
    file_code="UCSFFSX51_ADNI1_3T_02_01_16",                          # <-- VERIFICA
    source="UCSFFSX51_ADNI1_3T_02_01_16_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 1 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['LONISID']
    # + 373 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSX6
#   source: UCSFFSX6_11Aug2025.csv   |   righe campionate: 500   |   colonne: 346
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 13 colonne amministrative/QC (vedi IGNORE_* nello script)
#   325 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST101SV', 'ST102CV', 'ST102SA', 'ST102TA', 'ST102TS'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   382 | cand. ID
#     RID                      | num     |   382 | cand. ID
#     VISCODE                  | cat/str |     7 | cand. VISITA
#     VISCODE2                 | cat/str |    30 | cand. VISITA
#     EXAMDATE                 | date    |   404 | cand. DATA
#     RUNDATE                  | date    |   145 | cand. DATA
#     VERSION                  | date    |   145 | cand. DATA
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSX6 = DatasetConfig(
    file_code="UCSFFSX6",                          # <-- VERIFICA
    source="UCSFFSX6_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'VERSION', 'update_stamp']) VERIFICA
    # + 325 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSX7
#   source: UCSFFSX7_11Aug2025.csv   |   righe campionate: 500   |   colonne: 347
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 13 colonne amministrative/QC (vedi IGNORE_* nello script)
#   325 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST101SV', 'ST102CV', 'ST102SA', 'ST102TA', 'ST102TS'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   418 | cand. ID
#     RID                      | num     |   418 | cand. ID
#     VISCODE                  | cat/str |    22 | cand. VISITA
#     VISCODE2                 | cat/str |    28 | cand. VISITA
#     FIELD_STRENGTH           | cat/str |     2 | DA DECIDERE
#     EXAMDATE                 | date    |   451 | cand. DATA
#     RUNDATE                  | date    |    61 | cand. DATA
#     FSVER                    | date    |     2 | cand. DATA
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSX7 = DatasetConfig(
    file_code="UCSFFSX7",                          # <-- VERIFICA
    source="UCSFFSX7_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'FSVER', 'update_stamp']) VERIFICA
    # 1 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['FIELD_STRENGTH']
    # + 325 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UCSFFSX_11_02_15
#   source: UCSFFSX_11_02_15_11Aug2025.csv   |   righe campionate: 500   |   colonne: 366
#   INDIZIO categoria dal nome (NON deciso): ['csf', 'volumes']
#   ignorate 12 colonne amministrative/QC (vedi IGNORE_* nello script)
#   346 colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione
#     (es. ['ST100SV', 'ST101SV', 'ST102CV', 'ST102SA', 'ST102TA'] ...): non elencate qui, si mappano col dizionario
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |    85 | cand. ID
#     VISCODE                  | cat/str |    11 | cand. VISITA
#     EXAMDATE                 | date    |   370 | cand. DATA
#     VERSION                  | date    |   104 | cand. DATA
#     LONISID                  | num     |   457 | DA DECIDERE
#     FLDSTRENG                | num     |     1 | DA DECIDERE
#     RUNDATE                  | date    |   104 | cand. DATA
#     update_stamp             | date    |     7 | cand. DATA
# ------------------------------------------------------------------------
UCSFFSX_11_02_15 = DatasetConfig(
    file_code="UCSFFSX_11_02_15",                          # <-- VERIFICA
    source="UCSFFSX_11_02_15_11Aug2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf', 'volumes'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 2 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['LONISID', 'FLDSTRENG']
    # + 346 colonne ST* FreeSurfer da mappare col dizionario ADNI
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UGOTPTAU181_06_18_20
#   source: UGOTPTAU181_06_18_20_28Oct2025.csv   |   righe campionate: 500   |   colonne: 8
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   146 | cand. ID
#     VISCODE                  | cat/str |    12 | cand. VISITA
#     VISCODE2                 | cat/str |    12 | cand. VISITA
#     EXAMDATE                 | date    |   390 | cand. DATA
#     PLASMAPTAU181            | num     |   497 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UGOTPTAU181_06_18_20 = DatasetConfig(
    file_code="UGOTPTAU181_06_18_20",                          # <-- VERIFICA
    source="UGOTPTAU181_06_18_20_28Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['update_stamp']) VERIFICA
    # 1 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['PLASMAPTAU181']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNBIOMKADNIDIAN2017
#   source: UPENNBIOMKADNIDIAN2017_09Oct2025.csv   |   righe campionate: 422   |   colonne: 13
#   INDIZIO categoria dal nome (NON deciso): ['csf']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   184 | cand. ID
#     VISCODE                  | cat/str |    13 | cand. VISITA
#     VISCODE2                 | cat/str |    12 | cand. VISITA
#     EXAMDATE                 | date    |   384 | cand. DATA
#     STUDY                    | cat/str |     1 | DA DECIDERE
#     RUNDATE                  | date    |    14 | cand. DATA
#     ABETA                    | num     |   351 | DA DECIDERE
#     AB40                     | num     |   381 | DA DECIDERE
#     TAU                      | num     |   275 | DA DECIDERE
#     PTAU                     | num     |    81 | DA DECIDERE
#     A4240                    | num     |   273 | DA DECIDERE
#     NOTE                     | cat/str |     2 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENNBIOMKADNIDIAN2017 = DatasetConfig(
    file_code="UPENNBIOMKADNIDIAN2017",                          # <-- VERIFICA
    source="UPENNBIOMKADNIDIAN2017_09Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    # 7 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['STUDY', 'ABETA', 'AB40', 'TAU', 'PTAU', 'A4240', 'NOTE']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNBIOMK_MASTER
#   source: UPENNBIOMK_MASTER_23Oct2025.csv   |   righe campionate: 500   |   colonne: 14
#   INDIZIO categoria dal nome (NON deciso): ['csf']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |    65 | cand. ID
#     VISCODE                  | cat/str |     8 | cand. VISITA
#     BATCH                    | cat/str |     6 | DA DECIDERE
#     KIT                      | cat/str |     9 | DA DECIDERE
#     STDS                     | cat/str |     8 | DA DECIDERE
#     DRAWDTE                  | date    |   142 | cand. DATA
#     RUNDATE                  | date    |    45 | cand. DATA
#     ABETA                    | num     |   171 | DA DECIDERE
#     TAU                      | num     |   255 | DA DECIDERE
#     PTAU                     | num     |   212 | DA DECIDERE
#     ABETA_RAW                | num     |   203 | DA DECIDERE
#     TAU_RAW                  | num     |   266 | DA DECIDERE
#     PTAU_RAW                 | num     |   200 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENNBIOMK_MASTER = DatasetConfig(
    file_code="UPENNBIOMK_MASTER",                          # <-- VERIFICA
    source="UPENNBIOMK_MASTER_23Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    # date_column=?  candidati (dai valori): ['DRAWDTE', 'RUNDATE', 'update_stamp']  <-- DECIDI
    viscode_reference="VISCODE",
    # 9 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['BATCH', 'KIT', 'STDS', 'ABETA', 'TAU', 'PTAU', 'ABETA_RAW', 'TAU_RAW', 'PTAU_RAW']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNBIOMK_ROCHE_ELECSYS
#   source: UPENNBIOMK_ROCHE_ELECSYS_09Oct2025.csv   |   righe campionate: 500   |   colonne: 13
#   INDIZIO categoria dal nome (NON deciso): ['csf']
#   ignorate 2 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   196 | cand. ID
#     RID                      | num     |   196 | cand. ID
#     VISCODE2                 | cat/str |    12 | cand. VISITA
#     EXAMDATE                 | date    |   372 | cand. DATA
#     BATCH                    | cat/str |     4 | DA DECIDERE
#     RUNDATE                  | date    |    41 | cand. DATA
#     ABETA40                  | num     |    30 | DA DECIDERE
#     ABETA42                  | num     |   479 | DA DECIDERE
#     TAU                      | num     |   460 | DA DECIDERE
#     PTAU                     | num     |   469 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENNBIOMK_ROCHE_ELECSYS = DatasetConfig(
    file_code="UPENNBIOMK_ROCHE_ELECSYS",                          # <-- VERIFICA
    source="UPENNBIOMK_ROCHE_ELECSYS_09Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE2",
    # 5 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['BATCH', 'ABETA40', 'ABETA42', 'TAU', 'PTAU']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNMSMSABETA2CRM
#   source: UPENNMSMSABETA2CRM_23Oct2025.csv   |   righe campionate: 500   |   colonne: 11
#   ignorate 1 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   183 | cand. ID
#     VISCODE                  | cat/str |    13 | cand. VISITA
#     VISCODE2                 | cat/str |    11 | cand. VISITA
#     EXAMDATE                 | date    |   437 | cand. DATA
#     RUNDATE                  | date    |    64 | cand. DATA
#     ABETA42                  | num     |   423 | DA DECIDERE
#     ABETA40                  | num     |   488 | DA DECIDERE
#     ABETA38                  | num     |   444 | DA DECIDERE
#     ABETA42CRM               | num     |   415 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENNMSMSABETA2CRM = DatasetConfig(
    file_code="UPENNMSMSABETA2CRM",                          # <-- VERIFICA
    source="UPENNMSMSABETA2CRM_23Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    # 4 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['ABETA42', 'ABETA40', 'ABETA38', 'ABETA42CRM']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNMSMSABETA2
#   source: UPENNMSMSABETA2_23Oct2025.csv   |   righe campionate: 500   |   colonne: 10
#   ignorate 1 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   183 | cand. ID
#     VISCODE                  | cat/str |    13 | cand. VISITA
#     VISCODE2                 | cat/str |    12 | cand. VISITA
#     EXAMDATE                 | date    |   437 | cand. DATA
#     RUNDATE                  | date    |    64 | cand. DATA
#     ABETA42                  | num     |   423 | DA DECIDERE
#     ABETA40                  | num     |   488 | DA DECIDERE
#     ABETA38                  | num     |   444 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENNMSMSABETA2 = DatasetConfig(
    file_code="UPENNMSMSABETA2",                          # <-- VERIFICA
    source="UPENNMSMSABETA2_23Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    # 3 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['ABETA42', 'ABETA40', 'ABETA38']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNMSMSABETA
#   source: UPENNMSMSABETA_23Oct2025.csv   |   righe campionate: 400   |   colonne: 8
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   400 | cand. ID
#     VISCODE                  | cat/str |     1 | cand. VISITA
#     DRAWDATE                 | date    |   240 | cand. DATA
#     RUNDATE                  | date    |    17 | cand. DATA
#     ABETA42                  | num     |   358 | DA DECIDERE
#     ABETA40                  | num     |   387 | DA DECIDERE
#     ABETA38                  | num     |   355 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENNMSMSABETA = DatasetConfig(
    file_code="UPENNMSMSABETA",                          # <-- VERIFICA
    source="UPENNMSMSABETA_23Oct2025.csv",
    category=None,                              # <-- DECIDI
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="DRAWDATE",          # preferenza ADNI (alt: ['RUNDATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 3 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['ABETA42', 'ABETA40', 'ABETA38']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNPLASMA
#   source: UPENNPLASMA_28Oct2025.csv   |   righe campionate: 500   |   colonne: 5
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   125 | cand. ID
#     VISCODE                  | cat/str |     4 | cand. VISITA
#     AB40                     | num     |   424 | DA DECIDERE
#     AB42                     | num     |   271 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENNPLASMA = DatasetConfig(
    file_code="UPENNPLASMA",                          # <-- VERIFICA
    source="UPENNPLASMA_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: nessuna) VERIFICA
    date_column="update_stamp",                  # rilevato dai valori, VERIFICA
    viscode_reference="VISCODE",
    # 2 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['AB40', 'AB42']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENNROI_MARS_06_01_16
#   source: UPENNROI_MARS_06_01_16_09Oct2025.csv   |   righe campionate: 500   |   colonne: 269
#   INDIZIO categoria dal nome (NON deciso): ['volumes']
#   ignorate 1 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   500 | cand. ID
#     VISCODE                  | cat/str |     1 | cand. VISITA
#     EXAMDATE                 | date    |   227 | cand. DATA
#     VERSION                  | date    |     1 | cand. DATA
#     IMAGE_UID                | cat/str |   500 | DA DECIDERE
#     RUNDATE                  | date    |     1 | cand. DATA
#     CBICA_ID                 | cat/str |   500 | cand. ID
#     DATE                     | date    |   227 | cand. DATA
#     R702                     | num     |   498 | DA DECIDERE
#     R701                     | num     |   497 | DA DECIDERE
#     R601                     | num     |   499 | DA DECIDERE
#     R604                     | num     |   500 | DA DECIDERE
#     R606                     | num     |   500 | DA DECIDERE
#     R607                     | num     |   500 | DA DECIDERE
#     R613                     | num     |   497 | DA DECIDERE
#     R614                     | num     |   499 | DA DECIDERE
#     R501                     | num     |   497 | DA DECIDERE
#     R502                     | num     |   500 | DA DECIDERE
#     R503                     | num     |   498 | DA DECIDERE
#     R504                     | num     |   500 | DA DECIDERE
#     R505                     | num     |   498 | DA DECIDERE
#     R506                     | num     |   496 | DA DECIDERE
#     R507                     | num     |   499 | DA DECIDERE
#     R508                     | num     |   498 | DA DECIDERE
#     R509                     | num     |   499 | DA DECIDERE
#     R510                     | num     |   500 | DA DECIDERE
#     R511                     | num     |   500 | DA DECIDERE
#     R512                     | num     |   498 | DA DECIDERE
#     R513                     | num     |   499 | DA DECIDERE
#     R514                     | num     |   499 | DA DECIDERE
#     R515                     | num     |   499 | DA DECIDERE
#     R516                     | num     |   499 | DA DECIDERE
#     R517                     | num     |   500 | DA DECIDERE
#     R518                     | num     |   500 | DA DECIDERE
#     R519                     | num     |   498 | DA DECIDERE
#     R520                     | num     |   500 | DA DECIDERE
#     R521                     | num     |   499 | DA DECIDERE
#     R522                     | num     |   499 | DA DECIDERE
#     R523                     | num     |   498 | DA DECIDERE
#     R524                     | num     |   497 | DA DECIDERE
#     R525                     | num     |   500 | DA DECIDERE
#     R401                     | num     |   498 | DA DECIDERE
#     R402                     | num     |   497 | DA DECIDERE
#     R403                     | num     |   499 | DA DECIDERE
#     R404                     | num     |   499 | DA DECIDERE
#     R405                     | num     |   499 | DA DECIDERE
#     R406                     | num     |   498 | DA DECIDERE
#     R407                     | num     |   500 | DA DECIDERE
#     R408                     | num     |   500 | DA DECIDERE
#     R409                     | num     |   500 | DA DECIDERE
#     R410                     | num     |   498 | DA DECIDERE
#     R411                     | num     |   500 | DA DECIDERE
#     R412                     | num     |   500 | DA DECIDERE
#     R413                     | num     |   499 | DA DECIDERE
#     R414                     | num     |   500 | DA DECIDERE
#     R415                     | num     |   499 | DA DECIDERE
#     R416                     | num     |   500 | DA DECIDERE
#     R417                     | num     |   499 | DA DECIDERE
#     R418                     | num     |   499 | DA DECIDERE
#     R419                     | num     |   500 | DA DECIDERE
#     R420                     | num     |   499 | DA DECIDERE
#     R421                     | num     |   499 | DA DECIDERE
#     R422                     | num     |   500 | DA DECIDERE
#     R423                     | num     |   500 | DA DECIDERE
#     R424                     | num     |   499 | DA DECIDERE
#     R425                     | num     |   500 | DA DECIDERE
#     R426                     | num     |   499 | DA DECIDERE
#     R427                     | num     |   499 | DA DECIDERE
#     R428                     | num     |   499 | DA DECIDERE
#     R429                     | num     |   498 | DA DECIDERE
#     R430                     | num     |   499 | DA DECIDERE
#     R431                     | num     |   500 | DA DECIDERE
#     R432                     | num     |   499 | DA DECIDERE
#     R433                     | num     |   500 | DA DECIDERE
#     R434                     | num     |   500 | DA DECIDERE
#     R435                     | num     |   500 | DA DECIDERE
#     R436                     | num     |   500 | DA DECIDERE
#     R301                     | num     |   500 | DA DECIDERE
#     R302                     | num     |   498 | DA DECIDERE
#     R303                     | num     |   500 | DA DECIDERE
#     R304                     | num     |   500 | DA DECIDERE
#     R305                     | num     |   497 | DA DECIDERE
#     R306                     | num     |   500 | DA DECIDERE
#     R307                     | num     |   500 | DA DECIDERE
#     R308                     | num     |   500 | DA DECIDERE
#     R309                     | num     |   499 | DA DECIDERE
#     R310                     | num     |   499 | DA DECIDERE
#     R311                     | num     |   500 | DA DECIDERE
#     R312                     | num     |   498 | DA DECIDERE
#     R313                     | num     |   498 | DA DECIDERE
#     R314                     | num     |   500 | DA DECIDERE
#     R315                     | num     |   500 | DA DECIDERE
#     R316                     | num     |   499 | DA DECIDERE
#     R317                     | num     |   500 | DA DECIDERE
#     R318                     | num     |   500 | DA DECIDERE
#     R319                     | num     |   498 | DA DECIDERE
#     R320                     | num     |   500 | DA DECIDERE
#     R321                     | num     |   499 | DA DECIDERE
#     R322                     | num     |   500 | DA DECIDERE
#     R323                     | num     |   500 | DA DECIDERE
#     R324                     | num     |   499 | DA DECIDERE
#     R325                     | num     |   498 | DA DECIDERE
#     R326                     | num     |   500 | DA DECIDERE
#     R327                     | num     |   500 | DA DECIDERE
#     R328                     | num     |   499 | DA DECIDERE
#     R329                     | num     |   499 | DA DECIDERE
#     R330                     | num     |   500 | DA DECIDERE
#     R331                     | num     |   498 | DA DECIDERE
#     R332                     | num     |   499 | DA DECIDERE
#     R333                     | num     |   499 | DA DECIDERE
#     R334                     | num     |   500 | DA DECIDERE
#     R335                     | num     |   500 | DA DECIDERE
#     R336                     | num     |   495 | DA DECIDERE
#     R337                     | num     |   499 | DA DECIDERE
#     R338                     | num     |   499 | DA DECIDERE
#     R339                     | num     |   499 | DA DECIDERE
#     R340                     | num     |   500 | DA DECIDERE
#     R341                     | num     |   496 | DA DECIDERE
#     R342                     | num     |   499 | DA DECIDERE
#     R343                     | num     |   500 | DA DECIDERE
#     R344                     | num     |   500 | DA DECIDERE
#     R345                     | num     |   500 | DA DECIDERE
#     R4                       | num     |   499 | DA DECIDERE
#     R11                      | num     |   499 | DA DECIDERE
#     R23                      | num     |   500 | DA DECIDERE
#     R30                      | num     |   498 | DA DECIDERE
#     R31                      | num     |   500 | DA DECIDERE
#     R32                      | num     |   500 | DA DECIDERE
#     R35                      | num     |   499 | DA DECIDERE
#     R36                      | num     |   500 | DA DECIDERE
#     R37                      | num     |   497 | DA DECIDERE
#     R38                      | num     |   498 | DA DECIDERE
#     R39                      | num     |   498 | DA DECIDERE
#     R40                      | num     |   499 | DA DECIDERE
#     R41                      | num     |   497 | DA DECIDERE
#     R47                      | num     |   499 | DA DECIDERE
#     R48                      | num     |   497 | DA DECIDERE
#     R49                      | num     |   500 | DA DECIDERE
#     R50                      | num     |   499 | DA DECIDERE
#     R51                      | num     |   499 | DA DECIDERE
#     R52                      | num     |   500 | DA DECIDERE
#     R55                      | num     |   499 | DA DECIDERE
#     R56                      | num     |   494 | DA DECIDERE
#     R57                      | num     |   498 | DA DECIDERE
#     R58                      | num     |   500 | DA DECIDERE
#     R59                      | num     |   499 | DA DECIDERE
#     R60                      | num     |   500 | DA DECIDERE
#     R61                      | num     |   499 | DA DECIDERE
#     R62                      | num     |   499 | DA DECIDERE
#     R71                      | num     |   499 | DA DECIDERE
#     R72                      | num     |   500 | DA DECIDERE
#     R73                      | num     |   499 | DA DECIDERE
#     R75                      | num     |   500 | DA DECIDERE
#     R76                      | num     |   499 | DA DECIDERE
#     R81                      | num     |   498 | DA DECIDERE
#     R82                      | num     |   499 | DA DECIDERE
#     R83                      | num     |   499 | DA DECIDERE
#     R84                      | num     |   499 | DA DECIDERE
#     R85                      | num     |   500 | DA DECIDERE
#     R86                      | num     |   500 | DA DECIDERE
#     R87                      | num     |   500 | DA DECIDERE
#     R88                      | num     |   499 | DA DECIDERE
#     R89                      | num     |   499 | DA DECIDERE
#     R90                      | num     |   500 | DA DECIDERE
#     R91                      | num     |   500 | DA DECIDERE
#     R92                      | num     |   498 | DA DECIDERE
#     R93                      | num     |   500 | DA DECIDERE
#     R94                      | num     |   497 | DA DECIDERE
#     R95                      | num     |   497 | DA DECIDERE
#     R100                     | num     |   500 | DA DECIDERE
#     R101                     | num     |   500 | DA DECIDERE
#     R102                     | num     |   499 | DA DECIDERE
#     R103                     | num     |   499 | DA DECIDERE
#     R104                     | num     |   499 | DA DECIDERE
#     R105                     | num     |   498 | DA DECIDERE
#     R106                     | num     |   500 | DA DECIDERE
#     R107                     | num     |   499 | DA DECIDERE
#     R108                     | num     |   500 | DA DECIDERE
#     R109                     | num     |   499 | DA DECIDERE
#     R112                     | num     |   498 | DA DECIDERE
#     R113                     | num     |   500 | DA DECIDERE
#     R114                     | num     |   500 | DA DECIDERE
#     R115                     | num     |   500 | DA DECIDERE
#     R116                     | num     |   500 | DA DECIDERE
#     R117                     | num     |   499 | DA DECIDERE
#     R118                     | num     |   498 | DA DECIDERE
#     R119                     | num     |   497 | DA DECIDERE
#     R120                     | num     |   499 | DA DECIDERE
#     R121                     | num     |   498 | DA DECIDERE
#     R122                     | num     |   500 | DA DECIDERE
#     R123                     | num     |   499 | DA DECIDERE
#     R124                     | num     |   498 | DA DECIDERE
#     R125                     | num     |   498 | DA DECIDERE
#     R128                     | num     |   500 | DA DECIDERE
#     R129                     | num     |   500 | DA DECIDERE
#     R132                     | num     |   498 | DA DECIDERE
#     R133                     | num     |   497 | DA DECIDERE
#     R134                     | num     |   500 | DA DECIDERE
#     R135                     | num     |   500 | DA DECIDERE
#     R136                     | num     |   500 | DA DECIDERE
#     R137                     | num     |   499 | DA DECIDERE
#     R138                     | num     |   500 | DA DECIDERE
#     R139                     | num     |   500 | DA DECIDERE
#     R140                     | num     |   499 | DA DECIDERE
#     R141                     | num     |   498 | DA DECIDERE
#     R142                     | num     |   499 | DA DECIDERE
#     R143                     | num     |   499 | DA DECIDERE
#     R144                     | num     |   500 | DA DECIDERE
#     R145                     | num     |   500 | DA DECIDERE
#     R146                     | num     |   500 | DA DECIDERE
#     R147                     | num     |   500 | DA DECIDERE
#     R148                     | num     |   500 | DA DECIDERE
#     R149                     | num     |   500 | DA DECIDERE
#     R150                     | num     |   499 | DA DECIDERE
#     R151                     | num     |   499 | DA DECIDERE
#     R152                     | num     |   499 | DA DECIDERE
#     R153                     | num     |   500 | DA DECIDERE
#     R154                     | num     |   499 | DA DECIDERE
#     R155                     | num     |   500 | DA DECIDERE
#     R156                     | num     |   499 | DA DECIDERE
#     R157                     | num     |   498 | DA DECIDERE
#     R160                     | num     |   499 | DA DECIDERE
#     R161                     | num     |   500 | DA DECIDERE
#     R162                     | num     |   500 | DA DECIDERE
#     R163                     | num     |   500 | DA DECIDERE
#     R164                     | num     |   495 | DA DECIDERE
#     R165                     | num     |   499 | DA DECIDERE
#     R166                     | num     |   497 | DA DECIDERE
#     R167                     | num     |   500 | DA DECIDERE
#     R168                     | num     |   500 | DA DECIDERE
#     R169                     | num     |   500 | DA DECIDERE
#     R170                     | num     |   498 | DA DECIDERE
#     R171                     | num     |   500 | DA DECIDERE
#     R172                     | num     |   499 | DA DECIDERE
#     R173                     | num     |   498 | DA DECIDERE
#     R174                     | num     |   499 | DA DECIDERE
#     R175                     | num     |   499 | DA DECIDERE
#     R176                     | num     |   500 | DA DECIDERE
#     R177                     | num     |   499 | DA DECIDERE
#     R178                     | num     |   499 | DA DECIDERE
#     R179                     | num     |   498 | DA DECIDERE
#     R180                     | num     |   497 | DA DECIDERE
#     R181                     | num     |   499 | DA DECIDERE
#     R182                     | num     |   497 | DA DECIDERE
#     R183                     | num     |   497 | DA DECIDERE
#     R184                     | num     |   499 | DA DECIDERE
#     R185                     | num     |   500 | DA DECIDERE
#     R186                     | num     |   499 | DA DECIDERE
#     R187                     | num     |   500 | DA DECIDERE
#     R190                     | num     |   499 | DA DECIDERE
#     R191                     | num     |   497 | DA DECIDERE
#     R192                     | num     |   500 | DA DECIDERE
#     R193                     | num     |   500 | DA DECIDERE
#     R194                     | num     |   500 | DA DECIDERE
#     R195                     | num     |   499 | DA DECIDERE
#     R196                     | num     |   498 | DA DECIDERE
#     R197                     | num     |   498 | DA DECIDERE
#     R198                     | num     |   500 | DA DECIDERE
#     R199                     | num     |   500 | DA DECIDERE
#     R200                     | num     |   500 | DA DECIDERE
#     R201                     | num     |   500 | DA DECIDERE
#     R202                     | num     |   499 | DA DECIDERE
#     R203                     | num     |   500 | DA DECIDERE
#     R204                     | num     |   500 | DA DECIDERE
#     R205                     | num     |   499 | DA DECIDERE
#     R206                     | num     |   497 | DA DECIDERE
#     R207                     | num     |   500 | DA DECIDERE
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
UPENNROI_MARS_06_01_16 = DatasetConfig(
    file_code="UPENNROI_MARS_06_01_16",                          # <-- VERIFICA
    source="UPENNROI_MARS_06_01_16_09Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['volumes'])
    id_column="RID",                            # standard ADNI (alt: ['CBICA_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['VERSION', 'RUNDATE', 'DATE', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE",
    # 260 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['IMAGE_UID', 'R702', 'R701', 'R601', 'R604', 'R606', 'R607', 'R613', 'R614', 'R501', 'R502', 'R503', 'R504', 'R505', 'R506', 'R507', 'R508', 'R509', 'R510', 'R511', 'R512', 'R513', 'R514', 'R515', 'R516', 'R517', 'R518', 'R519', 'R520', 'R521', 'R522', 'R523', 'R524', 'R525', 'R401', 'R402', 'R403', 'R404', 'R405', 'R406', 'R407', 'R408', 'R409', 'R410', 'R411', 'R412', 'R413', 'R414', 'R415', 'R416', 'R417', 'R418', 'R419', 'R420', 'R421', 'R422', 'R423', 'R424', 'R425', 'R426', 'R427', 'R428', 'R429', 'R430', 'R431', 'R432', 'R433', 'R434', 'R435', 'R436', 'R301', 'R302', 'R303', 'R304', 'R305', 'R306', 'R307', 'R308', 'R309', 'R310', 'R311', 'R312', 'R313', 'R314', 'R315', 'R316', 'R317', 'R318', 'R319', 'R320', 'R321', 'R322', 'R323', 'R324', 'R325', 'R326', 'R327', 'R328', 'R329', 'R330', 'R331', 'R332', 'R333', 'R334', 'R335', 'R336', 'R337', 'R338', 'R339', 'R340', 'R341', 'R342', 'R343', 'R344', 'R345', 'R4', 'R11', 'R23', 'R30', 'R31', 'R32', 'R35', 'R36', 'R37', 'R38', 'R39', 'R40', 'R41', 'R47', 'R48', 'R49', 'R50', 'R51', 'R52', 'R55', 'R56', 'R57', 'R58', 'R59', 'R60', 'R61', 'R62', 'R71', 'R72', 'R73', 'R75', 'R76', 'R81', 'R82', 'R83', 'R84', 'R85', 'R86', 'R87', 'R88', 'R89', 'R90', 'R91', 'R92', 'R93', 'R94', 'R95', 'R100', 'R101', 'R102', 'R103', 'R104', 'R105', 'R106', 'R107', 'R108', 'R109', 'R112', 'R113', 'R114', 'R115', 'R116', 'R117', 'R118', 'R119', 'R120', 'R121', 'R122', 'R123', 'R124', 'R125', 'R128', 'R129', 'R132', 'R133', 'R134', 'R135', 'R136', 'R137', 'R138', 'R139', 'R140', 'R141', 'R142', 'R143', 'R144', 'R145', 'R146', 'R147', 'R148', 'R149', 'R150', 'R151', 'R152', 'R153', 'R154', 'R155', 'R156', 'R157', 'R160', 'R161', 'R162', 'R163', 'R164', 'R165', 'R166', 'R167', 'R168', 'R169', 'R170', 'R171', 'R172', 'R173', 'R174', 'R175', 'R176', 'R177', 'R178', 'R179', 'R180', 'R181', 'R182', 'R183', 'R184', 'R185', 'R186', 'R187', 'R190', 'R191', 'R192', 'R193', 'R194', 'R195', 'R196', 'R197', 'R198', 'R199', 'R200', 'R201', 'R202', 'R203', 'R204', 'R205', 'R206', 'R207']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# UPENN_PLASMA_FUJIREBIO_QUANTERIX
#   source: UPENN_PLASMA_FUJIREBIO_QUANTERIX_28Oct2025.csv   |   righe campionate: 500   |   colonne: 16
#   INDIZIO categoria dal nome (NON deciso): ['plasma', 'csf']
#   ignorate 3 colonne amministrative/QC (vedi IGNORE_* nello script)
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     PTID                     | cat/str |   372 | cand. ID
#     RID                      | num     |   372 | cand. ID
#     VISCODE                  | cat/str |    22 | cand. VISITA
#     VISCODE2                 | cat/str |    31 | cand. VISITA
#     EXAMDATE                 | date    |   454 | cand. DATA
#     pT217_F                  | num     |   379 | DA DECIDERE
#     AB42_F                   | num     |   451 | DA DECIDERE
#     AB40_F                   | num     |   489 | DA DECIDERE
#     AB42_AB40_F              | num     |   426 | DA DECIDERE
#     pT217_AB42_F             | num     |   487 | DA DECIDERE
#     NfL_Q                    | num     |   304 | DA DECIDERE
#     GFAP_Q                   | num     |   472 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
UPENN_PLASMA_FUJIREBIO_QUANTERIX = DatasetConfig(
    file_code="UPENN_PLASMA_FUJIREBIO_QUANTERIX",                          # <-- VERIFICA
    source="UPENN_PLASMA_FUJIREBIO_QUANTERIX_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma', 'csf'])
    id_column="RID",                            # standard ADNI (alt: ['PTID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['update_stamp']) VERIFICA
    # 7 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['pT217_F', 'AB42_F', 'AB40_F', 'AB42_AB40_F', 'pT217_AB42_F', 'NfL_Q', 'GFAP_Q']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# YASSINE_CSF
#   source: YASSINE_CSF_28Oct2025.csv   |   righe campionate: 188   |   colonne: 25
#   INDIZIO categoria dal nome (NON deciso): ['csf']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   188 | cand. ID
#     EXAMDATE                 | date    |   165 | cand. DATA
#     VISCODE2                 | cat/str |     1 | cand. VISITA
#     Sample_ID                | cat/str |   188 | cand. ID
#     Number                   | num     |    25 | DA DECIDERE
#     Type                     | cat/str |     1 | DA DECIDERE
#     Box                      | num     |     3 | DA DECIDERE
#     Order_in_Box             | num     |    73 | DA DECIDERE
#     MALDI                    | cat/str |   188 | DA DECIDERE
#     Date                     | date    |     3 | cand. DATA
#     Phenotype                | cat/str |     4 | DA DECIDERE
#     E2_level                 | num     |    12 | DA DECIDERE
#     E3_level                 | num     |    54 | DA DECIDERE
#     E4_level                 | num     |    42 | DA DECIDERE
#     E3_E2                    | num     |    12 | DA DECIDERE
#     E4_E3                    | num     |    35 | DA DECIDERE
#     E2_glyc                  | num     |    12 | DA DECIDERE
#     E3_glyc                  | num     |    97 | DA DECIDERE
#     E4_glyc                  | num     |    64 | DA DECIDERE
#     Total_glyc               | num     |   107 | DA DECIDERE
#     E2_2nd_glyc              | num     |    11 | DA DECIDERE
#     E3_2nd_glyc              | num     |    93 | DA DECIDERE
#     E4_2nd_glyc              | num     |    57 | DA DECIDERE
#     Total_2nd_glyc           | num     |    96 | DA DECIDERE
#     update_stamp             | date    |     1 | cand. DATA
# ------------------------------------------------------------------------
YASSINE_CSF = DatasetConfig(
    file_code="YASSINE_CSF",                          # <-- VERIFICA
    source="YASSINE_CSF_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['csf'])
    id_column="RID",                            # standard ADNI (alt: ['Sample_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['Date', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE2",
    # 19 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['Number', 'Type', 'Box', 'Order_in_Box', 'MALDI', 'Phenotype', 'E2_level', 'E3_level', 'E4_level', 'E3_E2', 'E4_E3', 'E2_glyc', 'E3_glyc', 'E4_glyc', 'Total_glyc', 'E2_2nd_glyc', 'E3_2nd_glyc', 'E4_2nd_glyc', 'Total_2nd_glyc']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

# ========================================================================
# YASSINE_PLASMA
#   source: YASSINE_PLASMA_28Oct2025.csv   |   righe campionate: 188   |   colonne: 22
#   INDIZIO categoria dal nome (NON deciso): ['plasma']
#   profilo colonne di interesse (nome | tipo | distinti | note):
#     RID                      | num     |   188 | cand. ID
#     EXAMDATE                 | date    |   157 | cand. DATA
#     VISCODE2                 | cat/str |     2 | cand. VISITA
#     Sample_ID                | cat/str |   188 | cand. ID
#     Number                   | num     |    25 | DA DECIDERE
#     Type                     | cat/str |     1 | DA DECIDERE
#     Box                      | num     |     3 | DA DECIDERE
#     Order_in_Box             | num     |    73 | DA DECIDERE
#     MALDI                    | cat/str |   188 | DA DECIDERE
#     Date                     | date    |     3 | cand. DATA
#     Phenotype                | cat/str |     6 | DA DECIDERE
#     E2_level                 | num     |    15 | DA DECIDERE
#     E3_level                 | num     |    62 | DA DECIDERE
#     E4_level                 | num     |    57 | DA DECIDERE
#     E3_E2                    | num     |    11 | DA DECIDERE
#     E4_E2                    | num     |     5 | DA DECIDERE
#     E4_E3                    | num     |    43 | DA DECIDERE
#     E2_glyc                  | num     |    16 | DA DECIDERE
#     E3_glyc                  | num     |   151 | DA DECIDERE
#     E4_glyc                  | num     |    87 | DA DECIDERE
#     Total_glyc               | num     |   171 | DA DECIDERE
#     update_stamp             | date    |     2 | cand. DATA
# ------------------------------------------------------------------------
YASSINE_PLASMA = DatasetConfig(
    file_code="YASSINE_PLASMA",                          # <-- VERIFICA
    source="YASSINE_PLASMA_28Oct2025.csv",
    category=None,                              # <-- DECIDI  (indizio: ['plasma'])
    id_column="RID",                            # standard ADNI (alt: ['Sample_ID']) VERIFICA
    date_column="EXAMDATE",          # preferenza ADNI (alt: ['Date', 'update_stamp']) VERIFICA
    viscode_reference="VISCODE2",
    # 16 colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):
    #   ['Number', 'Type', 'Box', 'Order_in_Box', 'MALDI', 'Phenotype', 'E2_level', 'E3_level', 'E4_level', 'E3_E2', 'E4_E2', 'E4_E3', 'E2_glyc', 'E3_glyc', 'E4_glyc', 'Total_glyc']
    # constant_columns={"METHOD_<CAT>": "<assay>"},   # se biomarcatore: METTI il metodo
    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)
)

DATASETS_DRAFT = {d.file_code: d for d in (
    ADAS,
    ADNI_DIAN_COMPARISON_STUDY_DATA_SUBSET_05_23_22,
    ADNIMERGE,
    ADNI_BLENNOWPLASMANFLLONG_10_03_18,
    ADNI_EUROIMMUN,
    ADNI_LIPIDOMICSRADER,
    ADNI_PICSLASHS,
    ADSP_PHC_BIOMARKER,
    AMPRION_ASYN_SAA,
    AMYREAD,
    APOERES,
    BAIPETNMRCFTP_08_17_22,
    BHR_SP_FAQ,
    BLCHANGE,
    BLENNOWCSFNFL,
    BLENNOWPLASMATAU,
    C2N_PRECIVITYAD2_PLASMA,
    CDR,
    CSFALPHASYN_03_21_14,
    DXSUM,
    FAQ,
    FNIH_PLASMA_PTAU_PROJECT,
    FUJIREBIOABETA,
    ITEM,
    MMSE,
    MOCA,
    NEUROBAT,
    NEUROPATH,
    PLASMA_ABETA_PROJECT_ADX_VUMC,
    PLASMA_ABETA_PROJECT_QUANTERIX,
    PLASMA_ABETA_PROJECT_ROCHE,
    PLASMA_ABETA_PROJECT_SHIMADZU,
    PLASMA_ABETA_PROJECT_U_OF_GOTHENBURG,
    PLASMA_ABETA_PROJECT_WASH_U_11_05_21,
    PTDEMOG,
    RMT_APOERES,
    RMT_ECOG12PT,
    RMT_ECOG12SP,
    RMT_PTDEMOG,
    RMT_SCREENING,
    SALADAX_BIOMEDICAL,
    UCBERKELEY_AMY_6MM,
    UCBERKELEY_TAUPVC_6MM,
    UCBERKELEY_TAU_6MM,
    UCD_ADNI1_WMH,
    UCD_WMH,
    UCSDVOL,
    UCSFFSL51ALL_08_01_16,
    UCSFFSL51Y1_08_01_16,
    UCSFFSL51_03_01_22,
    UCSFFSL_02_01_16,
    UCSFFSX51_11_08_19,
    UCSFFSX51_ADNI1_3T_02_01_16,
    UCSFFSX6,
    UCSFFSX7,
    UCSFFSX_11_02_15,
    UGOTPTAU181_06_18_20,
    UPENNBIOMKADNIDIAN2017,
    UPENNBIOMK_MASTER,
    UPENNBIOMK_ROCHE_ELECSYS,
    UPENNMSMSABETA2CRM,
    UPENNMSMSABETA2,
    UPENNMSMSABETA,
    UPENNPLASMA,
    UPENNROI_MARS_06_01_16,
    UPENN_PLASMA_FUJIREBIO_QUANTERIX,
    YASSINE_CSF,
    YASSINE_PLASMA,
)}
