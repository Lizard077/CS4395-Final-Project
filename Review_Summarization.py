import textwrap
import json
from transformers import pipeline
import sentencepiece
import torch
from bert_score import score


def load_data(data):
    with open(data) as data_f:
        unsplit_data = json.load(data_f)
    data_array = dict([])

    for elt in unsplit_data:
        mTitle = (elt["title"])
        mReview = ""
        for review in elt["reviews"]:
            mReview = mReview + " " + ((review["text"]))
        data_array[mTitle] = mReview
    return data_array


def print_summary(summaries, movie):
    wrapper = textwrap.TextWrapper(width=80, break_long_words=False, break_on_hyphens=False)
    print(movie, "generated summary:\n", wrapper.fill(summaries[movie]), "\n")


if __name__ == '__main__':
    data = load_data("HLT_data.json")

    summarization_pipeline = pipeline("summarization", model="abhiramd22/t5-base-finetuned-to-summarize-movie-reviews")
    summary = dict([])

    for i, movie in enumerate(data):
        output = summarization_pipeline(data[movie], clean_up_tokenization_spaces=True, max_length=256)
        summary[movie] = output[0]['summary_text']
        print("movie", movie, "complete")
        if (i == 9):
            break

    for i, movie in enumerate(data):
        print_summary(summary, movie)
        if (i == 9):
            break

reference_summaries = {
    "Tarzan": "Tarzan is a Disney animated adventure blending lush visuals, emotional depth, and Phil Collins' music, though it divides viewers over its pacing and character development.",

    "A Working Man": "A Working Man is a generic and uninspired action thriller despite Jason Statham’s efforts, criticized for its clichéd plot, excessive characters, and lack of innovation.",

    "Havoc": "Havoc is a gritty action film featuring Tom Hardy as a weary detective in a corrupt city, praised for its visuals and intense sequences but weighed down by a thin plot and heavy CGI use.",

    "Thunderbolts*": "Thunderbolts is a superhero film focused on trauma and redemption, offering character-driven storytelling and emotional depth, though reactions vary on its pacing and originality.",

    "A Minecraft Movie": "A Minecraft Movie is a nostalgic CGI adventure with retro aesthetics and a light-hearted plot aimed at younger audiences, mixing video game charm with sentimental storytelling.",

    "Death of a Unicorn": "Death of a Unicorn mixes dark comedy and fantasy with a mysterious creature subplot, showcasing potential but struggling with tonal consistency and character focus.",

    "Captain America: Brave New World": "This entry in the Marvel franchise features Sam Wilson stepping into the Captain America role with solid performances, though it’s held back by pacing issues and a predictable plot.",

    "In the Lost Lands": "In the Lost Lands is a fantasy adventure with imaginative visuals and strong leads, but the story is criticized for being derivative and lacking narrative clarity.",

    "Sinners": "Sinners is a supernatural horror set in 1930s Mississippi, blending blues culture with vampire folklore, praised for its music, atmosphere, and bold direction.",

    "The Monkey": "The Monkey is a horror-comedy with creative gore and a wacky premise, let down by flat characters and a weak story that doesn’t fully deliver on its potential."
}

generated_summaries = summary

references = []
candidates = []

for movie in generated_summaries:
    if movie in reference_summaries:
        candidates.append(generated_summaries[movie])
        references.append(reference_summaries[movie])

P, R, F1 = score(candidates, references, lang="en", verbose=True)

for i, movie in enumerate(generated_summaries):
    if i < len(F1):
        print(f"\n🎬 {movie}\nBERTScore F1: {F1[i].item():.4f}")
