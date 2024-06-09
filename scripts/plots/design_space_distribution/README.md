![design space distribution](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/bfe914f2-1543-458e-9f4f-06aa8cff871c)

    Generate Sobol Sequence Samples:
        The script uses the Sobol sequence to generate 500 low-discrepancy samples in a 2D space.
        These samples are used to simulate the generation of different geometry variants.

    Mock Meshes Generation:
        For demonstration purposes, the script uses the Sobol samples directly as mock data for geometry variants.

    Plotting the Results:
        Two scatter plots are created, each showing the distribution of the samples in a 2D design space.
        The plots are labeled "Approach_Angle" and "Decklid_Height" for the x-axes, with "Variable_1" and "Variable_2" for the y-axes, respectively.
