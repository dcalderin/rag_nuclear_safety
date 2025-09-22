
#################################################################
####---------Fermi 1024 model embedding implementation--------####
#################################################################

import itertools
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

# Load model ONCE at module level
model = AutoModelForMaskedLM.from_pretrained("atomic-canyon/fermi-1024")
tokenizer = AutoTokenizer.from_pretrained("atomic-canyon/fermi-1024")

# Tokenize input
# set the special tokens and id_to_token transform for post-process
special_token_ids = [tokenizer.vocab[token] for token in tokenizer.special_tokens_map.values()]
id_to_token = [""] * tokenizer.vocab_size
for token, _id in tokenizer.vocab.items():
    id_to_token[_id] = token

# get sparse vector from dense vectors with shape batch_size * seq_len * vocab_size
def get_sparse_vector(feature, output,special_token_ids):
    values, _ = torch.max(output*feature["attention_mask"].unsqueeze(-1), dim=1)
    values = torch.log(1 + torch.relu(values))
    values[:,special_token_ids] = 0
    return values
    
# transform the sparse vector to a dict of (token, weight)
def transform_sparse_vector_to_dict(sparse_vector, id_to_token):
    sample_indices,token_indices=torch.nonzero(sparse_vector,as_tuple=True)
    non_zero_values = sparse_vector[(sample_indices,token_indices)].tolist()
    number_of_tokens_for_each_sample = torch.bincount(sample_indices).cpu().tolist()
    tokens = [id_to_token[_id] for _id in token_indices.tolist()]

    output = []
    end_idxs = list(itertools.accumulate([0]+number_of_tokens_for_each_sample))
    for i in range(len(end_idxs)-1):
        token_strings = tokens[end_idxs[i]:end_idxs[i+1]]
        weights = non_zero_values[end_idxs[i]:end_idxs[i+1]]
        output.append(dict(zip(token_strings, weights)))
    return output


def get_fermi_sentence_embedding(text):
    # get the sparse vector
    feature = tokenizer([text], padding=True, truncation=True, return_tensors='pt', return_token_type_ids=False)
    output = model(**feature)[0]
    sparse_vector = get_sparse_vector(feature, output,special_token_ids)[0].detach().numpy()

    return sparse_vector
