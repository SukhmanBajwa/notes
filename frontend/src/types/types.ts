export interface UserData {
  pk: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}


export interface Course {
  id: string;
  user: number;
  name: string;
  is_archived: boolean;
  entry_count: number;
  summarised_count: number;
  open_action_count: number;
  latest_entry_title: string | null;
  latest_entry_date: string | null;
  client_updated_at: string;
  is_deleted: boolean;
  deleted_at: string | null;
  pg_created_at: string;
  pg_modified_at: string;
}


export interface CreatingCourse {
    name: string,
    is_archived: boolean,
    client_updated_at: string | null,
    is_deleted: boolean,
    deleted_at: string | null
}