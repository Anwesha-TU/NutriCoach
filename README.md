# NutriCoach

A Co-Pilot application which focuses on providing and explaining ingredient information of any food, prioritizing user experience and quality reasoning

## Description

-   NutriCoach can give consumers insights about ingredients found in labels of products they buy.

-   People usually have problems reading labels when they are deciding whether to buy a product or not.

-   Most of them have chemical labels which doesn't specify why an ingredient is added.

-   Here comes NutriCoach in action, it takes the ingredient lists as input, and explains what the ingredients mean and why they are added.

-   It explains the tradeoffs, and mentions if any healh issues are caused by the ingredients without making an absolute claims.

-   The model answers to the consumer with minimal input from the consumer.

-   This is what makes NutriCoach different from other AI-powered applications already available.

## Technologies Used

-   Frontend - **PyQt**

-   Backend - **Django**

-   AI - **RAG**

## Step-by-step Workflow

-   `Data Collection`: We collected about 20-30 ingredients details and saved them in **JSON** format.
-   `Data Preprocessing`: From the JSON data, the data was converted into numerical format with the help of an embedding model. These are called _Vecor Embeddings_.
-   `User Query`: Consumers paste their ingredients list and that becomes our user query. It is converted to numerical format with the same embedding model used to create vector embeddings.
-   `Retrieval`: **Cosine Similarity** is used to match the user query vector to all the embeddings and select the `k` closest matches. These k matches are our context.
-   `Generation`: Then, the generative model replies using the context, and if there is no context, then the model will say so without hallucinating.
