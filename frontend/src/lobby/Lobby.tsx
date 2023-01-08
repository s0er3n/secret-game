import {
  Accessor,
  Component,
  Show,
  splitProps,
  Setter,
  createSignal,
} from "solid-js";
import LobbyOverview from "./LobbyOverview";
import GameOver from "./GameOver";
import Wiki from "./Wiki";
import SetupGame from "./SetupGame";
import type { TLobby } from "../types";

export const [goToLobby, setGoToLobby] = createSignal(false);

export const isHost = (props: {
  id?: string;
  lobby: Accessor<TLobby | null>;
}) => {
  return props?.lobby()?.players[0][0].id == props.id && props.id; // checks for not null
};

const Lobby: Component<{
  setGoToLobby: Setter<boolean>;
  search: any;
  id: string | undefined;
  wiki: any;
  lobby: Accessor<TLobby | null>;
}> = (props) => {
  const [local, others] = splitProps(props, [
    "setGoToLobby",
    "lobby",
    "search",
    "id",
    "wiki",
  ]);

  return (
    <>
      <Show
        when={
          props?.lobby()?.state === "idle" &&
          !goToLobby() &&
          isHost({ lobby: props.lobby, id: props.id })
        }
      >
        <SetupGame id={local.id} lobby={local.lobby} search={local.search} />
      </Show>
      <Show
        when={
          (local.lobby()?.state === "idle" &&
            local.lobby()?.start_article &&
            goToLobby()) ||
          (!isHost(local) && local.lobby()?.state === "idle")
        }
      >
        <LobbyOverview lobby={local.lobby} id={local.id} />
      </Show>
      <Show when={local.lobby()?.state === "ingame"}>
        <Wiki wiki={local.wiki} />
      </Show>

      <Show when={local.lobby()?.state === "over"}>
        <GameOver local={local} players={local.lobby()?.players} />
      </Show>
    </>
  );
};

export default Lobby;
