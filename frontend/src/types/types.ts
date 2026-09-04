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


export interface NewCourse {
    name: string,
    is_archived: boolean,
    client_updated_at: string | null,
    is_deleted: boolean,
    deleted_at: string | null
}

export interface NewEntry {
    course: string;              
    title: string;
    body: string;
    lecture_date: string;        
    captured_at: string;         
    summary_text: string;
    summary_written_at: string | null;
    ai_summary_hidden: boolean;
    client_updated_at: string;
    is_deleted: boolean;
    deleted_at: string | null;
}