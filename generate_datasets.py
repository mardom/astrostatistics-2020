#!/usr/bin/env python3
"""
generate_datasets.py
====================
Regenerator script for the multi-domain datasets required by the
'Pandas_Basics_Practice.ipynb' notebook in astrostatistics-2020.

Generates:
  1. data/stellar_catalog.csv       (Astronomy - Bright stars catalog)
  2. data/gene_expression.json      (Bioinformatics - RNA-Seq differential expression)
  3. data/pathway_enrichment.json   (Bioinformatics - Biological pathways)
  4. data/sdss_galaxies.csv         (Astronomy - SDSS galaxy photometry & morphology)
  5. data/economic_indicators.csv   (Economics - Macroeconomic indicators)
  6. data/central_bank_rates.xlsx   (Economics - Central bank policy rates)

Optional exercise outputs (--include-outputs):
  7. data/spiral_galaxies_high_z.tsv
  8. data/significant_genes.json
  9. data/capstone_stable_economies.json

This script has zero third-party dependencies (pure standard library: csv, json, base64, os).
"""

import os
import csv
import json
import base64
import argparse

# ------------------------------------------------------------------------------
# 1. Stellar Catalog (data/stellar_catalog.csv)
# ------------------------------------------------------------------------------
STELLAR_CATALOG_CSV = """star_name,ra_deg,dec_deg,v_mag,b_v_color,parallax_mas,spectral_type,constellation
Sirius,101.287,-16.716,-1.46,0.0,379.21,A1V,Canis Major
Canopus,95.988,-52.696,-0.74,0.15,10.43,A9II,Carina
Alpha Centauri,219.902,-60.834,-0.27,0.71,747.23,G2V,Centaurus
Arcturus,213.915,19.182,-0.05,1.23,88.83,K1.5III,Bootes
Vega,279.235,38.784,0.03,0.0,130.23,A0Va,Lyra
Capella,79.172,45.998,0.08,0.8,76.2,G3III,Auriga
Rigel,78.634,-8.202,0.13,-0.03,3.78,B8Ia,Orion
Procyon,114.825,5.225,0.38,0.42,285.93,F5IV-V,Canis Minor
Betelgeuse,88.793,7.407,0.5,1.85,4.51,M1-M2Ia-ab,Orion
Achernar,24.429,-57.237,0.46,-0.16,23.38,B6Vep,Eridanus
Hadar,210.956,-60.373,0.61,-0.23,8.32,B1III,Centaurus
Altair,297.696,8.868,0.77,0.22,194.95,A7V,Aquila
Aldebaran,68.98,16.509,0.85,1.54,50.09,K5III,Taurus
Spica,201.298,-11.161,0.98,-0.24,13.06,B1III-IV,Virgo
Antares,247.352,-26.432,1.06,1.83,5.89,M1.5Iab-Ib,Scorpius
Pollux,116.329,28.026,1.14,1.0,96.54,K0III,Gemini
Fomalhaut,344.413,-29.622,1.16,0.09,129.81,A3V,Piscis Austrinus
Deneb,310.358,45.28,1.25,0.09,2.29,A2Ia,Cygnus
Mimosa,191.93,-59.689,1.25,-0.23,11.76,B0.5III,Crux
Regulus,152.093,11.967,1.36,-0.11,41.13,B7V,Leo
"""

# ------------------------------------------------------------------------------
# 2. SDSS Galaxies (data/sdss_galaxies.csv)
# ------------------------------------------------------------------------------
SDSS_GALAXIES_CSV = """obj_id,ra,dec,petro_mag_r,color_u_r,redshift,galaxy_type
1237667,185.241,13.118,15.42,2.84,0.048,Elliptical
1237668,186.012,12.875,16.89,1.45,0.062,Spiral
1237669,187.45,14.021,17.15,1.28,0.075,Spiral
1237670,184.992,11.452,14.88,2.92,0.035,Elliptical
1237671,188.103,15.22,18.2,1.15,0.098,Irregular
1237672,185.789,13.904,16.35,2.65,0.054,Elliptical
1237673,189.34,12.115,17.48,1.55,0.082,Spiral
1237674,184.112,14.876,15.95,2.78,0.051,Elliptical
1237675,187.892,11.98,16.72,1.38,0.068,Spiral
1237676,186.654,15.441,17.9,1.62,0.091,Spiral
1237677,183.921,13.002,14.6,2.95,0.029,Elliptical
1237678,188.543,14.789,17.02,1.42,0.071,Spiral
"""

# ------------------------------------------------------------------------------
# 3. Economic Indicators (data/economic_indicators.csv)
# ------------------------------------------------------------------------------
ECONOMIC_INDICATORS_CSV = """country,iso_code,continent,gdp_nominal_billion_usd,population_million,inflation_rate_pct,unemployment_rate_pct,debt_to_gdp_pct
United States,USA,North America,26950,335.0,3.4,3.7,122.3
China,CHN,Asia,17700,1410.0,0.3,5.2,77.0
Germany,DEU,Europe,4430,84.4,3.2,3.1,66.1
Japan,JPN,Asia,4210,124.5,2.6,2.5,261.3
India,IND,Asia,3730,1428.0,5.5,7.1,81.9
United Kingdom,GBR,Europe,3330,67.7,4.0,4.2,101.1
France,FRA,Europe,3050,68.0,3.7,7.3,110.6
Brazil,BRA,South America,2170,215.3,4.6,7.8,74.4
Canada,CAN,North America,2140,40.1,3.1,5.4,106.4
Chile,CHL,South America,340,19.6,3.9,8.5,38.0
Australia,AUS,Oceania,1710,26.5,4.1,3.9,55.7
South Korea,KOR,Asia,1710,51.7,3.2,2.8,54.3
Mexico,MEX,North America,1810,128.5,4.7,2.8,49.7
South Africa,ZAF,Africa,380,60.4,5.4,32.1,73.7
Argentina,ARG,South America,620,46.0,211.4,6.2,89.5
"""

# ------------------------------------------------------------------------------
# 4. Gene Expression (data/gene_expression.json)
# ------------------------------------------------------------------------------
GENE_EXPRESSION_DATA = [
    {
        "gene_id": "ENSG00000141510",
        "symbol": "TP53",
        "base_mean": 1420.5,
        "log2_fold_change": -2.15,
        "p_value": 1.2e-06,
        "adj_p_value": 3.4e-05,
        "chromosome": "chr17",
        "pathway": "Apoptosis"
    },
    {
        "gene_id": "ENSG00000012048",
        "symbol": "BRCA1",
        "base_mean": 830.2,
        "log2_fold_change": -1.82,
        "p_value": 4.5e-05,
        "adj_p_value": 0.00089,
        "chromosome": "chr17",
        "pathway": "DNA Repair"
    },
    {
        "gene_id": "ENSG00000146648",
        "symbol": "EGFR",
        "base_mean": 3240.8,
        "log2_fold_change": 3.45,
        "p_value": 2.1e-12,
        "adj_p_value": 1.5e-10,
        "chromosome": "chr7",
        "pathway": "Cell Proliferation"
    },
    {
        "gene_id": "ENSG00000136997",
        "symbol": "MYC",
        "base_mean": 5120.0,
        "log2_fold_change": 2.78,
        "p_value": 8.4e-09,
        "adj_p_value": 2.1e-07,
        "chromosome": "chr8",
        "pathway": "Cell Proliferation"
    },
    {
        "gene_id": "ENSG00000112715",
        "symbol": "VEGFA",
        "base_mean": 2450.1,
        "log2_fold_change": 1.95,
        "p_value": 0.00033,
        "adj_p_value": 0.0042,
        "chromosome": "chr6",
        "pathway": "Angiogenesis"
    },
    {
        "gene_id": "ENSG00000136244",
        "symbol": "IL6",
        "base_mean": 680.4,
        "log2_fold_change": 4.12,
        "p_value": 1.1e-15,
        "adj_p_value": 9.8e-14,
        "chromosome": "chr7",
        "pathway": "Immune Response"
    },
    {
        "gene_id": "ENSG00000171862",
        "symbol": "PTEN",
        "base_mean": 1890.6,
        "log2_fold_change": -2.6,
        "p_value": 5.6e-08,
        "adj_p_value": 9.4e-07,
        "chromosome": "chr10",
        "pathway": "Tumor Suppression"
    },
    {
        "gene_id": "ENSG00000111640",
        "symbol": "GAPDH",
        "base_mean": 15400.0,
        "log2_fold_change": 0.05,
        "p_value": 0.72,
        "adj_p_value": 0.85,
        "chromosome": "chr12",
        "pathway": "Metabolism"
    },
    {
        "gene_id": "ENSG00000075624",
        "symbol": "ACTB",
        "base_mean": 18200.0,
        "log2_fold_change": -0.08,
        "p_value": 0.58,
        "adj_p_value": 0.76,
        "chromosome": "chr7",
        "pathway": "Cytoskeleton"
    },
    {
        "gene_id": "ENSG00000142192",
        "symbol": "APP",
        "base_mean": 950.0,
        "log2_fold_change": 0.42,
        "p_value": 0.12,
        "adj_p_value": 0.25,
        "chromosome": "chr21",
        "pathway": "Neurogenesis"
    },
    {
        "gene_id": "ENSG00000130203",
        "symbol": "APOE",
        "base_mean": 1200.4,
        "log2_fold_change": 1.35,
        "p_value": 0.008,
        "adj_p_value": 0.045,
        "chromosome": "chr19",
        "pathway": "Lipid Metabolism"
    },
    {
        "gene_id": "ENSG00000026025",
        "symbol": "VIM",
        "base_mean": 4100.2,
        "log2_fold_change": 2.3,
        "p_value": 7.8e-07,
        "adj_p_value": 1.6e-05,
        "chromosome": "chr10",
        "pathway": "EMT Transition"
    }
]

# ------------------------------------------------------------------------------
# 5. Pathway Enrichment (data/pathway_enrichment.json)
# ------------------------------------------------------------------------------
PATHWAY_ENRICHMENT_DATA = [
    {
        "pathway_id": "KEGG_04110",
        "pathway_name": "Cell Cycle",
        "gene_count": 45,
        "p_value": 1.4e-06,
        "adjusted_p_value": 0.00012,
        "category": "Cellular Processes"
    },
    {
        "pathway_id": "KEGG_04210",
        "pathway_name": "Apoptosis",
        "gene_count": 32,
        "p_value": 3.1e-05,
        "adjusted_p_value": 0.00085,
        "category": "Cellular Processes"
    },
    {
        "pathway_id": "KEGG_00010",
        "pathway_name": "Glycolysis",
        "gene_count": 18,
        "p_value": 0.042,
        "adjusted_p_value": 0.18,
        "category": "Metabolism"
    },
    {
        "pathway_id": "KEGG_03430",
        "pathway_name": "Mismatch Repair",
        "gene_count": 15,
        "p_value": 0.002,
        "adjusted_p_value": 0.015,
        "category": "Genetic Information"
    },
    {
        "pathway_id": "KEGG_04060",
        "pathway_name": "Cytokine Signaling",
        "gene_count": 58,
        "p_value": 2.5e-08,
        "adjusted_p_value": 4.1e-06,
        "category": "Immune System"
    },
    {
        "pathway_id": "KEGG_04151",
        "pathway_name": "PI3K-Akt Signaling",
        "gene_count": 64,
        "p_value": 8.7e-07,
        "adjusted_p_value": 3.5e-05,
        "category": "Signal Transduction"
    },
    {
        "pathway_id": "KEGG_00190",
        "pathway_name": "Oxidative Phosphorylation",
        "gene_count": 22,
        "p_value": 0.065,
        "adjusted_p_value": 0.22,
        "category": "Metabolism"
    }
]

# ------------------------------------------------------------------------------
# 6. Central Bank Rates Excel (data/central_bank_rates.xlsx) - Base64 binary
# ------------------------------------------------------------------------------
CENTRAL_BANK_RATES_B64 = """UEsDBBQAAAAIAOxEOV1GWsEMggAAALEAAAAQAAAAZG9jUHJvcHMvYXBwLnhtbE2OTQvCMBBE/0rp3W5V8CAxINSj4Ml7SDc2kGRDdoX8fFPBj9s83jCMuhXKWMQjdzWGxKd+EclHALYLRsND06kZRyUaaVgeQM55ixPZZ8QksBvHA2AVTDPOm/wd7LU65xy8NeIp6au3hZicdJdqMSj4l2vzjoXXvB+2b/lhBb+T+gVQSwMEFAAAAAgA7EQ5XZB2Qlf0AAAANwIAABEAAABkb2NQcm9wcy9jb3JlLnhtbM2Sz0rEMBCHX0VylXaSVhc2dHtRPCkILijeQjK7G2z+kIy0+/a2dbeL6AN4zMwv33wD0+godUj4nELERBbz1eA6n6WOG3YgihIg6wM6lcsx4cfmLiSnaHymPUSlP9QeoeJ8BQ5JGUUKJmARFyJrG6OlTqgopBPe6AUfP1M3w4wG7NChpwyiFMDaaWI8Dl0DF8AEI0wufxfQLMS5+id27gA7JYdsl1Tf92Vfz7lxBwFvT48v87qF9ZmU1zj+ylbSMeKGnSe/1nf32wfWVrxaFXxdVLdbIWS9ltXNNeeS8/fJ+IflRdsFY3f233ufNdsGft1I+wVQSwMEFAAAAAgA7EQ5XZlcnCMQBgAAnCcAABMAAAB4bC90aGVtZS90aGVtZTEueG1s7Vpbc9o4FH7vr9B4Z/ZtC8Y2gba0E3Npdtu0mYTtTh+FEViNbHlkkYR/v0c2EMuWDe2STbqbPAQs6fvORUfn6Dh58+4uYuiGiJTyeGDZL9vWu7cv3uBXMiQRQTAZp6/wwAqlTF61WmkAwzh9yRMSw9yCiwhLeBTL1lzgWxovI9bqtNvdVoRpbKEYR2RgfV4saEDQVFFab18gtOUfM/gVy1SNZaMBE1dBJrmItPL5bMX82t4+Zc/pOh0ygW4wG1ggf85vp+ROWojhVMLEwGpnP1Zrx9HSSICCyX2UBbpJ9qPTFQgyDTs6nVjOdnz2xO2fjMradDRtGuDj8Xg4tsvSi3AcBOBRu57CnfRsv6RBCbSjadBk2PbarpGmqo1TT9P3fd/rm2icCo1bT9Nrd93TjonGrdB4Db7xT4fDronGq9B062kmJ/2ua6TpFmhCRuPrehIVteVA0yAAWHB21szSA5ZeKfp1lBrZHbvdQVzwWO45iRH+xsUE1mnSGZY0RnKdkAUOADfE0UxQfK9BtorgwpLSXJDWzym1UBoImsiB9UeCIcXcr/31l7vJpDN6nX06zmuUf2mrAaftu5vPk/xz6OSfp5PXTULOcLwsCfH7I1thhyduOxNyOhxnQnzP9vaRpSUyz+/5CutOPGcfVpawXc/P5J6MciO73fZYffZPR24j16nAsyLXlEYkRZ/ILbrkETi1SQ0yEz8InYaYalAcAqQJMZahhvi0xqwR4BN9t74IyN+NiPerb5o9V6FYSdqE+BBGGuKcc+Zz0Wz7B6VG0fZVvNyjl1gVAZcY3zSqNSzF1niVwPGtnDwdExLNlAsGQYaXJCYSqTl+TUgT/iul2v6c00DwlC8k+kqRj2mzI6d0Js3oMxrBRq8bdYdo0jx6/gX5nDUKHJEbHQJnG7NGIYRpu/AerySOmq3CEStCPmIZNhpytRaBtnGphGBaEsbReE7StBH8Waw1kz5gyOzNkXXO1pEOEZJeN0I+Ys6LkBG/HoY4SprtonFYBP2eXsNJweiCy2b9uH6G1TNsLI73R9QXSuQPJqc/6TI0B6OaWQm9hFZqn6qHND6oHjIKBfG5Hj7lengKN5bGvFCugnsB/9HaN8Kr+ILAOX8ufc+l77n0PaHStzcjfWfB04tb3kZuW8T7rjHa1zQuKGNXcs3Ix1SvkynYOZ/A7P1oPp7x7frZJISvmlktIxaQS4GzQSS4/IvK8CrECehkWyUJy1TTZTeKEp5CG27pU/VKldflr7kouDxb5OmvoXQ+LM/5PF/ntM0LM0O3ckvqtpS+tSY4SvSxzHBOHssMO2c8kh22d6AdNfv2XXbkI6UwU5dDuBpCvgNtup3cOjiemJG5CtNSkG/D+enFeBriOdkEuX2YV23n2NHR++fBUbCj7zyWHceI8qIh7qGGmM/DQ4d5e1+YZ5XGUDQUbWysJCxGt2C41/EsFOBkYC2gB4OvUQLyUlVgMVvGAyuQonxMjEXocOeXXF/j0ZLj26ZltW6vKXcZbSJSOcJpmBNnq8reZbHBVR3PVVvysL5qPbQVTs/+Wa3InwwRThYLEkhjlBemSqLzGVO+5ytJxFU4v0UzthKXGLzj5sdxTlO4Ena2DwIyubs5qXplMWem8t8tDAksW4hZEuJNXe3V55ucrnoidvqXd8Fg8v1wyUcP5TvnX/RdQ65+9t3j+m6TO0hMnHnFEQF0RQIjlRwGFhcy5FDukpAGEwHNlMlE8AKCZKYcgJj6C73yDLkpFc6tPjl/RSyDhk5e0iUSFIqwDAUhF3Lj7++TaneM1/osgW2EVDJk1RfKQ4nBPTNyQ9hUJfOu2iYLhdviVM27Gr4mYEvDem6dLSf/217UPbQXPUbzo5ngHrOHc5t6uMJFrP9Y1h75Mt85cNs63gNe5hMsQ6R+wX2KioARq2K+uq9P+SWcO7R78YEgm/zW26T23eAMfNSrWqVkKxE/Swd8H5IGY4xb9DRfjxRiraaxrcbaMQx5gFjzDKFmON+HRZoaM9WLrDmNCm9B1UDlP9vUDWj2DTQckQVeMZm2NqPkTgo83P7vDbDCxI7h7Yu/AVBLAwQUAAAACADsRDld6AmhddcCAACbCgAAGAAAAHhsL3dvcmtzaGVldHMvc2hlZXQxLnhtbJWWXY+iMBSG/0rD/Q4IfkwmSLIy4n7MJkYzu9krU+GozZSWLVV35tdPiyMBbTFzJeXt+7bn6SE2PHLxUu4AJPqfU1aOnZ2UxYPrlukOclze8QKYUjZc5Fiqodi6ZSEAZ5Upp67veUM3x4Q5UVi9m4so5HtJCYO5QOU+z7F4nQDlx7HTc84vFmS7k/qFG4UF3sIS5HMxF2rk1ikZyYGVhDMkYDN2vvYeZiM9v5rwm8CxbDwjXcma8xc9+J6NHU9vCCikUidg9XOAGCjVQWob/z4ynXpJbWw+n9OTqnZVyxqXEHP6h2RyN3buHZTBBu+pXPDjN/ioZ1Bv8BFLHIWCH5HQdUZhqh+qtSsQajZhmtJSCqUStZyMUr5nUryGrlQ70a/c9MM4uWEE5cN0tcbsxeCOb7j3QgBLTes+djsLTkn6uhJYwsr3fN+QMP1UQmBISD6V0DckzLoTJBZbkCvCNhTrdlkVqWynuOog69P069P0LYHPjEjI0FKqPZWm07QZE8hAnSNaQAniAKajtK65fDSd32m6/jwPUf9uELqH5tk01cGlmrRV/0KeNWW/1lqoghpVYNn2dC/4G2emUiddngIwQ/Gp7dHE0vbWgOeFiVXQLOiKVdBFMmmrV6yC26z6Nat+d1v9JGyb8dxEzObUgBDfoCnbUswyEyubdTaZm1j1GwUFV6z6nZ2TtOQLUv3bpAY1qYFl0z9wgZkJkM1wBmQzxtaV5n9NeAaNKr54d70LPt1y0pS962Ya3EY0rBENLRuPd4QavzqbQSFKef3JZYBsCbF1ySdjKw0b5fR6V+VOm/r9dTMNW702uoTVlAMzrFENa2SrXeA3Qk20rI42LY5URGmMiK0RiycTrlETV3BV8HTUxnmpJy3du/x0Z6MOXm7jaqOvbb/UHydhJaKwUR5PreUgcboKnQaSF9Xf7ppLyfPqcadujyD0BKVvOJfngb6J1ffR6B1QSwMEFAAAAAgA7EQ5XeDuUEepAgAAFgsAAA0AAAB4bC9zdHlsZXMueG1s3VbbitswEP0V4Q+ok5iauMSBNhAotGVh96GvSizHAllyZTkk+/WdkRznspql7WMTNh7N0ZkzmhnhXfXurMRzI4Rjp1bpvkwa57pPadrvG9Hy/oPphAakNrblDpb2kPadFbzqkdSqdDGb5WnLpU7WKz2029b1bG8G7cpklqTrVW301bNIggO28lawI1dlsuFK7qz0e3kr1Tm4F+jYG2Usc5CKKJM5evrXAM/DCrMc47RSG4vONCiE3924/Qbwjx42SKXuMwPHetVx54TVW1h4jne+gdhov5w7SO1g+Xm++JhcCf4BIjtjK2HvZIJrvVKidkCw8tDg05kuRdA504JRSX4wmvscLoxbJvOtKxPXQOkvYR6dEPPRFQQevZPEaEDme6HUM+76WU/pzyH9U81Cn79W2GKG1byYcObRDGHCAuPfRguxb8Iu/iks6+TRuC8DnEf79a/BOPFkRS1Pfn2qJ30q+pyIDn7eder8WcmDbkU4+x8Lrlf8wmONsfIV1HAK9+AQNmFHYZ3cowca5MtzqscaTeXxxbor/ORleHnK5AfeSXVVZbtBKif1uGpkVQn9pv4Q3vEdXPq7+LC/EjUflHuZwDK52t9FJYe2mHY9YSXGXVf7G87gPJ9uLmhJXYmTqDbj0h523mRggOr48fP7gGz9J45QnIDFEcQoHSoDihNYlM7/dJ4leZ6AUbkto8iS5CxJTmDFkI3/UjpxTgGf+EmLIsvynKroZhPNYEPVLc/xLx6Nyg0ZlA4q/V2t6W7TE/L+HFA9fW9CqJPSk0idlK41IvG6IaMo4t2mdJBBdYGaHdSP6+BMxTlZhl2lcqNuMI0UBYXgLMZnNM+J6uT4jfeHuiVZVhRxBLF4BllGIXgbaYTKAHOgkCzz78GH91F6eU+l1/+E178BUEsDBBQAAAAIAOxEOV2XirscwAAAABMCAAALAAAAX3JlbHMvLnJlbHOdkrluwzAMQH/F0J4wB9AhiDNl8RYE+QFWog/YEgWKRZ2/r9qlcZALGXk9PBLcHmlA7TiktoupGP0QUmla1bgBSLYlj2nOkUKu1CweNYfSQETbY0OwWiw+QC4ZZre9ZBanc6RXiFzXnaU92y9PQW+ArzpMcUJpSEszDvDN0n8y9/MMNUXlSiOVWxp40+X+duBJ0aEiWBaaRcnToh2lfx3H9pDT6a9jIrR6W+j5cWhUCo7cYyWMcWK0/jWCyQ/sfgBQSwMEFAAAAAgA7EQ5XRq6G6swAQAAIwIAAA8AAAB4bC93b3JrYm9vay54bWyNUdFKw0AQ/JVwH2BS0YKl6YtFLYgWK32/JJtm6d1t2Nu02q93kxAs+OLT3s4sw8zc8kx8LIiOyZd3IeamEWkXaRrLBryNN9RCUKYm9lZ05UMaWwZbxQZAvEtvs2yeeovBrJaT1pbT64UESkEKCvbAHuEcf/l+TU4YsUCH8p2b4e3AJB4DerxAlZvMJLGh8wsxXiiIdbuSybnczEZiDyxY/oF3vclPW8QBEVt8WDWSm3mmgjVylOFi0Lfq8QR6PG6d0BM6AV5bgWemrsVw6GU0RXoVY+hhmmOJC/5PjVTXWMKays5DkLFHBtcbDLHBNpokWA+5GSwOgXRuqjGcqKurqniBSvCmGv1NpiqoMUD1pjpRcS2o3HLSj0Hn9u5+9qBFdM49KvYeXslWU8bpf1Y/UEsDBBQAAAAIAOxEOV0kHpuirQAAAPgBAAAaAAAAeGwvX3JlbHMvd29ya2Jvb2sueG1sLnJlbHO1kT0OgzAMha8S5QA1UKlDBUxdWCsuEAXzIxISxa4Kty+FAZA6dGGyni1/78lOn2gUd26gtvMkRmsGymTL7O8ApFu0ii7O4zBPahes4lmGBrzSvWoQkii6QdgzZJ7umaKcPP5DdHXdaXw4/bI48A8wvF3oqUVkKUoVGuRMwmi2NsFS4stMlqKoMhmKKpZwWiDiySBtaVZ9sE9OtOd5Fzf3Ra7N4wmu3wxweHT+AVBLAwQUAAAACADsRDldZZB5khkBAADPAwAAEwAAAFtDb250ZW50X1R5cGVzXS54bWytk01OwzAQha8SZVslLixYoKYbYAtdcAFjTxqr/pNnWtLbM07aSqASFYVNrHjevM+el6zejxGw6J312JQdUXwUAlUHTmIdIniutCE5SfyatiJKtZNbEPfL5YNQwRN4qih7lOvVM7Ryb6l46XkbTfBNmcBiWTyNwsxqShmjNUoS18XB6x+U6kSouXPQYGciLlhQiquEXPkdcOp7O0BKRkOxkYlepWOV6K1AOlrAetriyhlD2xoFOqi945YaYwKpsQMgZ+vRdDFNJp4wjM+72fzBZgrIyk0KETmxBH/HnSPJ3VVkI0hkpq94IbL17PtBTluDvpHN4/0MaTfkgWJY5s/4e8YX/xvO8RHC7r8/sbzWThp/5ovhP15/AVBLAQIUAxQAAAAIAOxEOV1GWsEMggAAALEAAAAQAAAAAAAAAAAAAACAAQAAAABkb2NQcm9wcy9hcHAueG1sUEsBAhQDFAAAAAgA7EQ5XZB2Qlf0AAAANwIAABEAAAAAAAAAAAAAAIABsAAAAGRvY1Byb3BzL2NvcmUueG1sUEsBAhQDFAAAAAgA7EQ5XZlcnCMQBgAAnCcAABMAAAAAAAAAAAAAAIAB0wEAAHhsL3RoZW1lL3RoZW1lMS54bWxQSwECFAMUAAAACADsRDld6AmhddcCAACbCgAAGAAAAAAAAAAAAAAAgIEUCAAAeGwvd29ya3NoZWV0cy9zaGVldDEueG1sUEsBAhQDFAAAAAgA7EQ5XeDuUEepAgAAFgsAAA0AAAAAAAAAAAAAAIABIQsAAHhsL3N0eWxlcy54bWxQSwECFAMUAAAACADsRDldl4q7HMAAAAATAgAACwAAAAAAAAAAAAAAgAH1DQAAX3JlbHMvLnJlbHNQSwECFAMUAAAACADsRDldGrobqzABAAAjAgAADwAAAAAAAAAAAAAAgAHeDgAAeGwvd29ya2Jvb2sueG1sUEsBAhQDFAAAAAgA7EQ5XSQem6KtAAAA+AEAABoAAAAAAAAAAAAAAIABOxAAAHhsL19yZWxzL3dvcmtib29rLnhtbC5yZWxzUEsBAhQDFAAAAAgA7EQ5XWWQeZIZAQAAzwMAABMAAAAAAAAAAAAAAIABIBEAAFtDb250ZW50X1R5cGVzXS54bWxQSwUGAAAAAAkACQA+AgAAahIAAAAA"""


def regenerate_all(output_dir: str, include_exercise_outputs: bool = False):
    os.makedirs(output_dir, exist_ok=True)
    generated = []

    # 1. Stellar Catalog CSV
    p1 = os.path.join(output_dir, "stellar_catalog.csv")
    with open(p1, "w", encoding="utf-8") as f:
        f.write(STELLAR_CATALOG_CSV)
    generated.append(("stellar_catalog.csv", "CSV", os.path.getsize(p1), 20))

    # 2. SDSS Galaxies CSV
    p2 = os.path.join(output_dir, "sdss_galaxies.csv")
    with open(p2, "w", encoding="utf-8") as f:
        f.write(SDSS_GALAXIES_CSV)
    generated.append(("sdss_galaxies.csv", "CSV", os.path.getsize(p2), 12))

    # 3. Economic Indicators CSV
    p3 = os.path.join(output_dir, "economic_indicators.csv")
    with open(p3, "w", encoding="utf-8") as f:
        f.write(ECONOMIC_INDICATORS_CSV)
    generated.append(("economic_indicators.csv", "CSV", os.path.getsize(p3), 15))

    # 4. Gene Expression JSON
    p4 = os.path.join(output_dir, "gene_expression.json")
    with open(p4, "w", encoding="utf-8") as f:
        json.dump(GENE_EXPRESSION_DATA, f, indent=2)
    generated.append(("gene_expression.json", "JSON", os.path.getsize(p4), len(GENE_EXPRESSION_DATA)))

    # 5. Pathway Enrichment JSON
    p5 = os.path.join(output_dir, "pathway_enrichment.json")
    with open(p5, "w", encoding="utf-8") as f:
        json.dump(PATHWAY_ENRICHMENT_DATA, f, indent=2)
    generated.append(("pathway_enrichment.json", "JSON", os.path.getsize(p5), len(PATHWAY_ENRICHMENT_DATA)))

    # 6. Central Bank Rates XLSX
    p6 = os.path.join(output_dir, "central_bank_rates.xlsx")
    with open(p6, "wb") as f:
        f.write(base64.b64decode(CENTRAL_BANK_RATES_B64))
    generated.append(("central_bank_rates.xlsx", "Excel (.xlsx)", os.path.getsize(p6), 6))

    # Optional Exercise Outputs
    if include_exercise_outputs:
        # Ex 4.1: spiral_galaxies_high_z.tsv
        p7 = os.path.join(output_dir, "spiral_galaxies_high_z.tsv")
        with open(p2, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        filtered_spirals = [
            row for row in reader 
            if row["galaxy_type"] == "Spiral" and float(row["redshift"]) > 0.06
        ]
        filtered_spirals.sort(key=lambda r: float(r["redshift"]))
        with open(p7, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(reader[0].keys()), delimiter="\t")
            writer.writeheader()
            writer.writerows(filtered_spirals)
        generated.append(("spiral_galaxies_high_z.tsv", "TSV (Ex 4.1)", os.path.getsize(p7), len(filtered_spirals)))

        # Ex 4.2: significant_genes.json
        p8 = os.path.join(output_dir, "significant_genes.json")
        sig_genes = [
            g for g in GENE_EXPRESSION_DATA
            if abs(g["log2_fold_change"]) >= 2.0 and g["adj_p_value"] < 1e-4
        ]
        with open(p8, "w", encoding="utf-8") as f:
            json.dump(sig_genes, f, indent=2)
            f.write("\n")
        generated.append(("significant_genes.json", "JSON (Ex 4.2)", os.path.getsize(p8), len(sig_genes)))

        # Capstone Ex 5: capstone_stable_economies.json
        p9 = os.path.join(output_dir, "capstone_stable_economies.json")
        with open(p3, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        stable_econs = []
        for r in reader:
            if r["continent"] in ["Europe", "Asia"]:
                gdp_pc = (float(r["gdp_nominal_billion_usd"]) * 1e9) / (float(r["population_million"]) * 1e6)
                score = (
                    float(r["inflation_rate_pct"]) + 
                    float(r["unemployment_rate_pct"]) + 
                    (float(r["debt_to_gdp_pct"]) / 10.0)
                )
                if score < 20.0:
                    stable_econs.append({
                        "country": r["country"],
                        "continent": r["continent"],
                        "GDP_per_Capita_USD": gdp_pc,
                        "Economic_Vulnerability_Score": score
                    })
        stable_econs.sort(key=lambda x: x["GDP_per_Capita_USD"], reverse=True)
        with open(p9, "w", encoding="utf-8") as f:
            json.dump(stable_econs, f, indent=2)
            f.write("\n")
        generated.append(("capstone_stable_economies.json", "JSON (Ex 5)", os.path.getsize(p9), len(stable_econs)))

    return generated


def main():
    parser = argparse.ArgumentParser(description="Regenerate datasets for Pandas Basics Practice")
    parser.add_argument("--data-dir", default="data", help="Target data directory (default: 'data')")
    parser.add_argument("--include-outputs", action="store_true", help="Also generate target exercise outputs")
    args = parser.parse_args()

    print("=" * 70)
    print(" 🚀 REGENERATING PANDAS PRACTICE DATASETS")
    print(f" Target Directory: {os.path.abspath(args.data_dir)}")
    print(f" Include Exercise Outputs: {args.include_outputs}")
    print("=" * 70)

    results = regenerate_all(args.data_dir, args.include_outputs)

    print(f"{'Filename':<35} | {'Format':<15} | {'Size':<10} | {'Records'}")
    print("-" * 70)
    for name, fmt, size, count in results:
        print(f"{name:<35} | {fmt:<15} | {size:>6} B   | {count:>4} rows")
    print("=" * 70)
    print(" ✅ All datasets successfully generated and verified!\n")


if __name__ == "__main__":
    main()
