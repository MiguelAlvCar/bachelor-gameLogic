# Requirements
- conda 25.3.1 

# Initial setup
- To install the dependencies in a new environment:
    ```sh
    conda env create -f environment.yml
    ```

# Install new dependencies
- edit file `environment.yml`
- activate the environment in anaconda prompt:
    ```sh
    conda activate nn-gameLogic
    ```
- run:
    ```sh
    conda env update -f environment.yml
    ```

# Test the application
- run mypy:
    ```sh
    mypy .
    ```
