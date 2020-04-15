To get the full text from a uwazi instance
mongoexport --db uwazi_development --collection files --type=json --fields fullText  --out test.json

Then run the script
python3 create_model/preprocess.py

Then create the model using fasttext

Install and setup fasttext:  [link](https://fasttext.cc/docs/en/supervised-tutorial.html)

then run
./fasttext skipgram -input text.txt -output model_name -minn 3 -maxn 6 -dim 100