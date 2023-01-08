import { Component, For, Show } from "solid-js";
import Article from "../Article";
import { TPlayer } from "../types";
import { sendMessage } from "./../App";
import { isHost } from "./Lobby";

type Props = {
  players: TPlayer[] | undefined;
  // TOOD: invastigae whats happening here
  local: any;
};

const GameOver: Component<Props> = (props) => {
  if (!props.players) return <></>;
  return (
    <div>
      <ul>
        <For
          each={
            props.players.sort(
              (a: TPlayer, b: TPlayer) =>
                (b[0]?.points ?? 0) - (a[0]?.points ?? 0) ?? []
            ) ?? []
          }
        >
          {(player) => (
            <li>
              <span>{player[0].name} : </span>
              <span>{player[0].points}</span>
              <ol>
                <For each={player[1].moves?.map((move) => move.pretty_name)}>
                  {(article) => (
                    <li>
                      <Article title={article} />
                    </li>
                  )}
                </For>
              </ol>
            </li>
          )}
        </For>
      </ul>

      <Show when={isHost(props.local)}>
        <p>
          <button
            class="btn mt-3"
            onclick={() => {
              sendMessage({ type: "game", method: "go_to_lobby", args: {} });
            }}
          >
            go to lobby
          </button>
        </p>
      </Show>
    </div>
  );
};

export default GameOver;
