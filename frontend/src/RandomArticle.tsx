import { Component } from "solid-js";

const RandomArticle: Component<{ setter: (random_article: string) => void }> = (
  props
) => {
  let random_articles: string[] = [];
  return (
    <button
      class="btn"
      onclick={async () => {
        if (random_articles.length === 0) {
          try {
            let response = await fetch(
              "https://en.wikipedia.org/w/api.php?action=query&list=random&format=json&rnnamespace=0&rnlimit=100&origin=*"
            );
            let data = (await response.json()) as {
              query: { random: { title: string }[] };
            };
            random_articles = data.query.random.map((e) => e.title);
          } catch (e) {
            alert(e);
          }
        }
        if (random_articles.length !== 0) {
          let article = random_articles.pop();
          if (article) {
            props.setter(article);
          }
        }
      }}
    >
      get random article name
    </button>
  );
};
export default RandomArticle;
