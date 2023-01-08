export interface TLobby {
  method: string;
  end_time: number;
  state: string;
  id: string;
  players: TPlayer[];
  articles_to_find: string[];
  articles_found: any[];
  start_article: string;
  time: number;
}

export type TPlayer = [
  {
    id?: string;
    name?: string;
    points?: number;
  },
  {
    rights?: string;
    state?: string;
    moves?: TArticle[];
  }
];

export interface TArticle {
  url_name: string;
  pretty_name: string;
}

export interface TWikiUpdate {
  method: string;
  data: TWiki;
}

export interface TWiki {
  links: string[];
  title: string;
  content_html: string;
  url_ending: string;
}
