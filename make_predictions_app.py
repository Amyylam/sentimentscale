import streamlit as st

import pandas as pd
import numpy as np
from flair.models import TextClassifier
from flair.data import Sentence

##checkpt: Jun6 8:31pm done prediction and reading dataframe!

new_data_folder = './'
finetuned_classifier = TextClassifier.load(new_data_folder + 'best-model.pt')

def finetuned_model_predictions(input_file_path, finetuned_classifier, output_file_path):
  '''Makes Sentiment Predictions on unannotated data points contained in the input csvfile by loading the user-defined classifier.
     Exports the csvfile by adding new columns and filling in results from model predictions.
  '''


  unannotated_df = pd.read_csv(input_file_path)
  ## drop some duplicated rows
  unannotated_df = unannotated_df.drop_duplicates('title_desc')


  ## add new columns to export predictions
  ## modified on May28 to export predict_prob for less likely labels as well
  unannotated_df['confidence_1'] = None
  unannotated_df['confidence_-1'] = None
  unannotated_df['confidence_0'] = None
  unannotated_df['best_label'] = None
  unannotated_df['best_confidence'] = None
  unannotated_df['second_likely'] = None
  unannotated_df['second_confidence'] = None
  unannotated_df['least_likely'] = None
  unannotated_df['least_confidence'] = None



  for i in range(len(unannotated_df)):

    #print(unannotated_df['title_desc'].iloc[i])
    sentence = Sentence(unannotated_df['title_desc'].iloc[i])

    finetuned_classifier.predict(sentence,  multi_class_prob=True)
    ## predict_prob example: [1 (0.0002), -1 (0.9997), 0 (0.0001)]

    #print(sentence.labels)

    unannotated_df['confidence_1'].iloc[i] = sentence.labels[0].score
    unannotated_df['confidence_-1'].iloc[i] = sentence.labels[1].score
    unannotated_df['confidence_0'].iloc[i] = sentence.labels[2].score

    pred_confs = [sentence.labels[c].score for c in range(len(sentence.labels))]

    best_label_ind = np.argmax(pred_confs)
    best_confidence = np.max(pred_confs)
    second_likely_ind = np.argsort(pred_confs)[-2] # array in ascending order
    second_likely_confidence = np.sort(pred_confs)[-2]
    least_likely_ind = np.argsort(pred_confs)[0]
    least_likely_confidence = np.sort(pred_confs)[0]

    label_dict = {0:1,1:-1,2:0} ### this predict_prob order varies depending on the finetuned_classifier's initialization

    unannotated_df['best_label'].iloc[i] = label_dict[best_label_ind]
    unannotated_df['best_confidence'].iloc[i] = best_confidence
    #print(label_dict[best_label_ind],best_confidence)
    unannotated_df['second_likely'].iloc[i] = label_dict[second_likely_ind]
    unannotated_df['second_confidence'].iloc[i] = second_likely_confidence
    unannotated_df['least_likely'].iloc[i] = label_dict[least_likely_ind]
    unannotated_df['least_confidence'].iloc[i] = least_likely_confidence


  print(f"All { len(unannotated_df) } rows done prediction! ")

  unannotated_df.to_csv(output_file_path,index=False)

  print("Done export!")

  return unannotated_df['best_label'].value_counts()




def text_predictions(string, finetuned_classifier):
    sentence = Sentence(string)
    finetuned_classifier.predict(sentence,  multi_class_prob=True)

    pred_dict = {sentence.labels[c].value:sentence.labels[c].score for c in range(len(sentence.labels))}

    
    return pred_dict


#reference: df Styler documentation -- https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

## start layout

st.header("Business News Sentiment Analyzer")

title = st.text_input('Input a news headline: ', '')
st.write('Sentiment prediction probability distribution is', text_predictions(title, finetuned_classifier))


# reference from documentation -- https://docs.streamlit.io/en/latest/api.html#display-interactive-widgets

uploaded_file = st.file_uploader("Choose a CSV file to do predictions", type="csv")

if uploaded_file:
    #data_to_predict = pd.read_csv(uploaded_file)
    output_path = 'prediction.csv'
    finetuned_model_predictions(uploaded_file, finetuned_classifier, output_path)
    data_predicted = pd.read_csv(output_path)
    data_predicted = data_predicted[['title_desc','best_label','best_confidence','second_likely','second_confidence']]
    data_styler= data_predicted.style.hide_index().applymap(color_negative_red,subset=['best_label','second_likely'])
    
    st.dataframe(data_styler)