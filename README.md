# receiptParse
ICS 438 UHM

# components:
1. Prompt convert tex to structured data \n
	Tests:
		Make sure it generates correct data
		Make sure you handle edge cases
			missing data
			data not in the correct type (like phone number is (808).. instead of as a number)
			LLM returning text or invalid JSON
2. Identify category for vender
	Get embeddings for title and ingredients then do KNN or something
	Tests:
		Make sure it predicts 1 of the 7 categories and also that it gives the correct categories

3. Identify category of embeddings
		

