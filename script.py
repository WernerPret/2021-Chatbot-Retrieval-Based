from collections import Counter
from responses import responses, blank_spot
from user_functions import preprocess, compare_overlap, pos_tag, extract_nouns, compute_similarity
import spacy
word2vec = spacy.load('en')

exit_commands = ("quit", "goodbye", "exit", "no", "leave")

class ChatBot: 
  #define .make_exit() below:
  def exit_command(self, user_message):
    for command in exit_commands:
      if command in user_message:
        print("Goodbye")
        return True
   

  #define .chat() below:
  def chat(self):
    user_message = input("Welcome to le cyborg cantina\n>")
    while not self.exit_command(user_message):
      result = self.respond(user_message)
    

  #define .find_intent_match() below:
  def find_match_intent(self, responses, user_message):
    bow_user_message = Counter(preprocess(user_message))
    bow_responses = [Counter(preprocess(response)) for response in responses]
    similarity_list = [compare_overlap(response, user_message) for response in bow_responses]
    response_index = similarity_list.index(max(similarity_list))
    return responses[response_index]

  #define .find_entities() below:
  def find_entities(self, user_message):
    processed_pos_user_message = pos_tag(preprocess(user_message))
    message_nouns = extract_nouns(processed_pos_user_message)
    tokens = word2vec(" ".join(message_nouns))
    category = word2vec("blank_spot")
    word2vec_result = compute_similarity(tokens, category)
    word2vec_result.sort(key=lambda x: x[2])
    if len(word2vec_result) > 0:
      return word2vec_result[-1][0]
    else: return blank_spot
 
  #define .respond() below:
  def respond(self, user_message):
    best_response = self.find_match_intent(responses, user_message)
    entity = self.find_entities(user_message)
    final = best_response.format(entity)
    print(final)
    
    return self.chat()
  

#initialize ChatBot instance below:
cantina = ChatBot()
#call .chat() method below:
cantina.chat()


