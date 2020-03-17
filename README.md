## Classificazione dei gradi di demenza / alzheimer da MRI + CSF

#### Preprocessing
* Skull stripping (ROBEX)
* N4 (ANTS)
* Intensity Normalization (Fuzzy c-means)
* CROP (nilearn)
* Registrazione affine (Plastimatch)

Tutta la parte di preprocessing si trova in /utils/preprocessing
