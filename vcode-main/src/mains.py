import torch
import random
from transformers import AutoTokenizer, AutoModelForSequenceClassification
# Placeholder for recognize_speech() function
def recognize_speech():
    # Your speech recognition logic here
    pass

class SentimentAnalyzer:
    def __init__(self):
        # Model selection (consider alternatives if necessary)
        self.model_name = "bert-base-uncased-finetuned-sst-2-english"  # Double-check the name

        # Authentication (if using a private repository)
        if self.model_name.startswith("private/"):  # Adjust this check if necessary
            from huggingface_hub import cached_download  # Assuming you have huggingface_hub installed
            token = "<your_huggingface_token>"  # Replace with your valid token
            with cached_download(token=token):
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        else:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            except Exception as e:  # Catch any exception during model loading
                print(f"Error loading tokenizer or model: {e}")
                exit()

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment of the provided text using the loaded model.

        Args:
            text (str): The text to analyze.

        Returns:
            tuple: A tuple containing the predicted sentiment (positive, neutral, negative)
                   and the corresponding confidence score.
        """

        encoded_text = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**encoded_text)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)

        sentiment_labels = {0: "negative", 1: "neutral", 2: "positive"}
        predicted_sentiment = sentiment_labels[predictions.item()]
        confidence = torch.nn.functional.softmax(logits, dim=-1).max().item()

        return predicted_sentiment, confidence

    def respond_to_user(self, sentiment, confidence):
        """
        Generates a response based on the user's sentiment and confidence score.

        Args:
            sentiment (str): The predicted sentiment (positive, neutral, negative).
            confidence (float): The confidence score for the sentiment prediction.
        """

        positive_responses = [
            "That sounds great! How can I help you with that?",
            "I'm happy to hear it! Is there anything you'd like me to do?",
            "What would you like to do next?"
        ]
        neutral_responses = [
            "Interesting. Tell me more about it.",
            "Okay, how can I be of service?",
            "What would you like to do next?"
        ]
        negative_responses = [
            "Oh no, that's not good. How can I help you feel better?",
            "I understand that you're feeling down. Is there anything I can do to support you?",
            "Don't worry, things will get better. Let me know if you need someone to talk to."
        ]

        if sentiment == "positive" and confidence > 0.7:
            response = random.choice(positive_responses)
        elif sentiment == "negative" and confidence > 0.7:
            response = random.choice(negative_responses)
        else:
            response = random.choice(neutral_responses)

        print("Mani Bob: " + response)

def main():
    """
    Main loop to handle user interaction.
    """

    analyzer = SentimentAnalyzer()  # Create                                        an instance of the SentimentAnalyzer

    while True:
        text = recognize_speech()
        if not text:  # Exit loop if no speech is recognized
            break

        sentiment, confidence = analyzer.analyze_sentiment(text)
        analyzer.respond_to_user(sentiment, confidence)

if __name__ == "__main__":
    main()
