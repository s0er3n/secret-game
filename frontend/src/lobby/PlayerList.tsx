import { Component, For } from "solid-js";
import { TPlayer } from "../types";

const PlayerList: Component<{ players: TPlayer[] }> = (props) => {
  return (
    <For
      each={props.players.sort(
        (a: TPlayer, b: TPlayer) =>
          (b[0]?.points ?? 0) - (a[0]?.points ?? 0) ?? []
      )}
    >
      {(player: TPlayer) => (
        <>
          <span> {player[0].name} : </span>
          <span> {JSON.stringify(player[0].points ?? 0)}</span>
        </>
      )}
    </For>
  );
};

export default PlayerList;
