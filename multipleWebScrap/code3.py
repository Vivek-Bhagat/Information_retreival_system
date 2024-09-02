# %%
import pandas as pd
from nltk import word_tokenize
df = pd.read_csv('nature_articless.csv')
df.head()


# %%
tokens=[]
for index,row in df.iterrows():
    words = row['Title'].lower().split()
    for word in words:
        if word not in tokens:
            tokens.append(word)


print(tokens)

# %%
vector_title=[]

# %%
for index, row in df.iterrows():
    words = row['Title'].lower().split()
    vector_one=[]
    for token in tokens:
        if token in words:
            vector_one.append(1)
        else:
            vector_one.append(0)
    vector_title.append(vector_one)
print(vector_title)

# %%
dataframe = pd.DataFrame(vector_title, columns=tokens)
dataframe.head()

# %%
dataframe.shape

# %%
token_frequency=[]

# %%
sorted_token = sorted(tokens)
print(sorted_token)

# %%
for index, row in df.iterrows():
    words = row['Title'].lower().split()
    token_freq = 0
    for token in sorted_token:
        if token in words:
            token_freq += 1
    token_frequency.append(token_freq)

print(token_frequency)


# %%
#posting_list = []
#for token in sorted_token:
    #words = row['Title'].lower().split()
    #p_list = ""
    #for word in words:
        #if word == token and  "1 -->" not in p_list:
            #p_list += "1 -->"
    #posting_list.append(p_list)

# %%

sorted_token = sorted(set(token for title in df['Title'].dropna() for token in title.lower().split()))

posting_lists = {token: [] for token in sorted_token}

# Build posting lists
for index, row in df.iterrows():
    words = set(row['Title'].lower().split())  # Convert title words to a set for fast lookup
    for token in sorted_token:
        if token in words:
            posting_lists[token].append(f"{index} -->")

# Convert posting lists to the desired format
posting_list = {token: ''.join(posting_lists[token]) for token in sorted_token}




# %%
posting_list

# %%

pd.DataFrame(list(posting_list.items()), columns=['Token', 'Posting List']).to_csv('posting_list.csv', index=False)

# %%
input_search = input('Enter the string to search :')

# Convert the input search string into tokens
search_tokens = input_search.lower().split()

filter_from_posting_list = []

# Collect postings for each search token
for token in search_tokens:
    if token in posting_list:
        filter_from_posting_list.append(posting_list[token])
    else:
        filter_from_posting_list.append('')  

# Merge the postings from all search tokens
merged_postings = ' '.join(filter_from_posting_list)

print("Merged Postings:", merged_postings)

# %%



