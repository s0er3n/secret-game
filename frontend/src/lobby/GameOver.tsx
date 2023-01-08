import { Component, For, Show } from "solid-js";
import { sendMessage } from "./../App";
import { isHost } from "./Lobby";

type Props = {
  players: any[];
};

const GameOver: Component<Props> = (props) => {
  return (
    <div class="flex justify-center">
      <div>
        <ul>
          <For each={props.players ?? []}>
            {(player, i) => (
              <li>
                <div class="flex flex-row">
                  <div class="font-bold">{player[0].name}</div>
                  <div class="ml-2 ">{player[0].points}</div>
                  <div class="ml-2 ">
                    {player[1].moves
                      .map((move: any) => move.pretty_name)
                      .join(" -> ")}
                  </div>
                </div>
              </li>
            )}
          </For>
        </ul>

        <Show when={isHost(props.local)}>
          <button
            class="btn mt-3"
            onclick={() => {
              sendMessage({ type: "game", method: "go_to_lobby", args: {} });
            }}
          >
            go to lobby
          </button>
        </Show>
      </div>
    </div>
  );
};

export default GameOver;
