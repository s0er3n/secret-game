import { Component } from "solid-js";
import { sendMessage } from "./../App";
import "./../wiki.css";

const Wiki: Component<{ wiki: any }> = (props) => {
  return (
    <div>
      <h1>{props.wiki()?.title ?? ""}</h1>
      <div
        onclick={async (e) => {
          let targetValue = e.target.getAttribute("href");
          if (
            targetValue?.includes("wiki") &&
            !targetValue?.includes("wiki/Help") &&
            !targetValue?.includes("wiki/File")
          ) {
            e.preventDefault();

            let moveMsg = {
              type: "game",
              method: "move",
              args: {
                url_name: targetValue?.split("wiki/").pop(),
              },
            };
            sendMessage(moveMsg);
          } else if (
            targetValue?.includes("http") ||
            targetValue?.includes("wiki")
          ) {
            e.preventDefault();
            return;
          }
        }}
        innerHTML={props.wiki()?.content_html ?? ""}
      />
    </div>
  );
};

export default Wiki;
