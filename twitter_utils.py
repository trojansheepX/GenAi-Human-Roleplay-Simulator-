import pickle
import pandas as pd

# Function to load data from pickle files
def load_data(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

# Function to create instruction from post title and context
def create_instruction(post_title, context=""):
    instruction = f"Here is a post titled '{post_title}'.\n"
    if context:
        instruction += f"Context: {context}\n"
    instruction += "Can you generate a random human comment for this post?"
    return instruction

# Function to process the dataset and create the training pairs
def create_dataset_format(platform_comments, output_file):
    dataset = []
    
    for post_title, comments in platform_comments.items():
        # Use the first few words from the first comment to generate some context if needed
        context = " ".join(comments[0].split()[:15]) if comments else ""
        
        for comment in comments:
            # Skip empty or invalid comments
            if not comment.strip():
                continue
            
            # Create the instruction and formatted sample
            instruction = create_instruction(post_title, context)
            formatted_sample = f"<s>[INST] {instruction} [/INST] {comment}</s>"
            
            # Append the formatted sample to the dataset
            dataset.append(formatted_sample)
    
    # Save the dataset to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        for sample in dataset:
            f.write(sample + "\n")



# Function to load the dataset from the generated text file
def load_dataset_from_file(file_name):
    dataset = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            dataset.append(line.strip())  # Read and strip each line (removes newlines)
    return dataset

# Function to convert the dataset into a DataFrame and save it as a CSV file
def save_dataset_to_csv(dataset, output_file):
    # Split the data into instruction and answer for each entry
    instructions = []
    answers = []

    for entry in dataset:
        # Extract the instruction (inside [INST] and [/INST]) and the answer (after [/INST])
        try:
            instruction_start = entry.index('[INST]') + len('[INST]')
            instruction_end = entry.index('[/INST]')
            instruction = entry[instruction_start:instruction_end].strip()

            answer_start = instruction_end + len('[/INST]')
            answer = entry[answer_start:].strip()

            instructions.append(instruction)
            answers.append(answer)
        except ValueError:
            # Handle cases where the format might not be as expected
            print(f"Skipping improperly formatted entry: {entry}")
            continue

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        'Instruction': instructions,
        'Answer': answers
    })

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False, encoding='utf-8')
