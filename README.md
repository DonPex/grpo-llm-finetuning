# grpo-llm-finetuning
Fine-tuning of LLM using GRPO technique for text-to-sql context

## How to Run the Training Notebook

To fine-tune the model using the GRPO technique, follow these steps:

1. **Environment Setup**:
   - Ensure you have a machine with at least one GPU.
   - Install the required dependencies.

2. **Prepare the Dataset**:
   - The `data/` directory contains the datasets required for training:
     - `full-dataset.jsonl`: The complete dataset for training.
     - `questions-hard.txt` and `questions-simple.txt`: Text files with sample questions.
     - `rawdata-ddl.sql` and `tmf724_incident_management-ddl.sql`: SQL schema definitions.
   - Ensure the datasets are properly formatted and placed in the `data/` directory.

3. **Run the Notebook**:
   - Open the `train.ipynb` notebook in Jupyter or any compatible environment.
   - Execute the cells sequentially to start the training process.

4. **Training Details**:
   - The training process uses the GRPO (Guided Reward Policy Optimization) technique, as described in [this article](https://blog.gopenai.com/fine-tuning-a-text-to-sql-llm-for-reasoning-using-grpo-ec2c1b55278f).
   - The notebook is configured to fine-tune a 7B parameter LLM for text-to-SQL tasks, focusing on reasoning and SQL accuracy.

## Additional Information

- **Dataset Details**:
  - The dataset has been generated through Gemini 2.5 pro. It is based on `questions-simple.txt` and on `rawdata` schema data.
    First, a list of sample questions (simple and hard) has been generated.
    Then, a set of SQL queries and necessary context to execute that query have been generated.

- **Reference**:
  - For more details on the GRPO technique and its application to text-to-SQL tasks, refer to the [original article](https://blog.gopenai.com/fine-tuning-a-text-to-sql-llm-for-reasoning-using-grpo-ec2c1b55278f).

