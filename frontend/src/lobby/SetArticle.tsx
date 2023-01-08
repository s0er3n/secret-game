import { Accessor, Component, createSignal, For, Show } from "solid-js";
import { sendMessage } from "./../App";
import RandomArticle from "./../RandomArticle";

let [article, setArticle] = createSignal("");

const SetArticle: Component<{
  lobby: Accessor<any>;
  search: Accessor<Array<Array<string>> | undefined>;
}> = (props) => {
  let timeout: any = null;
  return (
    <div class="flex flex-row justify-center ">
      <div>
        <input
          class="input input-bordered"
          onkeyup={(e: any) => {
            if (timeout != null) {
              clearTimeout(timeout);
            }
            timeout = setTimeout(() => {
              const searchMsg = {
                type: "search",
                method: "execute",
                args: {
                  query: e.target.value,
                },
              };
              sendMessage(searchMsg);

              setArticle(e.target.value);
            }, 200);
          }}
          value={article()}
        />
        <RandomArticle
          setter={(random_article: string) => {
            const searchMsg = {
              type: "search",
              method: "execute",
              args: {
                query: random_article,
              },
            };
            sendMessage(searchMsg);
            setArticle(random_article);
          }}
        />

        <Show when={article() !== ""}>
          <ArticleSuggestionsList search={props.search} lobby={props.lobby} />
        </Show>
      </div>
    </div>
  );
};

const ArticleSuggestionsList: Component<{
  lobby: Accessor<any>;
  search: Accessor<Array<Array<string>> | undefined>;
}> = (props) => {
  return (
    <ul>
      <For each={props.search ? props?.search()?.at(3) ?? [] : []}>
        {(result, i) => (
          <li class="mt-2">
            <span> {props.search()?.at(1)?.at(i())} </span>
            <button
              onclick={() => {
                let setArticleMsg = {
                  type: "game",
                  method: "set_article",
                  args: {
                    article: result.split("/").pop(),
                    better_name: props.search()?.at(1)?.at(i()),
                    start: props.lobby().start_article === "",
                  },
                };
                sendMessage(setArticleMsg);
                setArticle("");
              }}
              class="btn"
            >
              select
            </button>
          </li>
        )}
      </For>
    </ul>
  );
};
export default SetArticle;
