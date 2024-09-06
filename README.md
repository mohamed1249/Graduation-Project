# AI-Powered Mental Health Assistant System for Autism and ADHD Diagnosis

## Introduction

This project aims to develop an AI-powered solution using Large Language Models (LLMs) to assist individuals, families, and professionals in better understanding and diagnosing Autism Spectrum Disorder (ASD) and Attention-Deficit/Hyperactivity Disorder (ADHD). The AI system leverages advanced natural language processing (NLP) techniques to analyze mental health data, providing insights, guidance, and suggestions.

## Table of Contents
- [Introduction](#introduction)
- [Motivation](#motivation)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Results](#results)
- [Future Work](#future-work)
- [Contributors](#contributors)
- [License](#license)

## Motivation

With the growing need for accessible and efficient mental health services, particularly in diagnosing and managing Autism and ADHD, this project aims to bridge the gap between patients and mental health professionals. By creating an AI tool that understands and processes symptoms, behaviors, and treatment methods, we hope to provide immediate, accessible information and support to those in need.

## Technologies Used

- **Python**: Primary programming language.
- **OpenAI API (GPT-3.5, GPT-4)**: Used for developing and fine-tuning large language models.
- **PHP & MySQL**: For system login data storing.
- **LangChain**: For building pipelines to manage LLM interactions.
- **Gradio**: To develop user-friendly web interfaces for real-time model interaction.
- **JavaScript & HTML**: For developing the Front-End.
- **Flask**: For developing the API to connect the LLMs to the Front-End.

## Features

- **Diagnosis Support**: The AI model provides information and analysis to help users better understand symptoms and diagnosis processes for ASD and ADHD.
- **Educational Resources**: Offers personalized suggestions based on users' inputs, pointing them towards relevant research or medical guidelines.
- **Natural Language Processing**: Allows for smooth, conversational interactions with users, offering detailed responses in plain language.
- **User Interface**: Gradio&HTML-powered interfaces for easy interaction with the AI system.


## Methodology

1. **Data Collection**: Used mental health datasets, including the DSM-5 and medical research papers on Autism and ADHD.
2. **Preprocessing**: Cleaned and formatted textual data using NLP techniques, including tokenization, stemming, and stopword removal.
3. **Model Building**: Fine-tuned GPT-3.5 and GPT-4 models on the preprocessed mental health data using supervised learning.
4. **Evaluation**: Evaluated model performance using standard NLP metrics, such as accuracy, perplexity, and F1-score.
5. **Deployment**: Deployed the AI system on GCP with a user interface built using Gradio for easy interaction.

## Results

The AI model effectively provides diagnostic insights and educational guidance on Autism and ADHD, producing accurate and context-aware responses based on users’ inputs. Initial testing showed a significant improvement in accessibility and understanding of mental health issues compared to traditional resources.

## Future Work

- **Additional Diagnoses**: Expand the model to include other mental health disorders like depression, anxiety, and OCD.
- **Multilingual Support**: Add support for languages other than English to make the tool accessible worldwide.
- **Enhanced Personalization**: Implement more advanced personalization features based on user-specific data to improve interaction quality.

## Contributors

- **Mohammad Abdulsalam** (Project Owner)
  
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

