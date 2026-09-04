import { NewEntry } from "../types/types"
import { fetchWithAuth } from "./fetchWithAuth"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"



const useAEntry =(id:string) => {
    const entry = useQuery({
        queryKey: ["entry",id],
        queryFn: () => fetchAnEntry(id),
    })
    return {entry}
}


// add error check inside the states

const useGetAllEntries = () => {
    const entries = useQuery({
        queryKey: ["entries"],
        queryFn: fetchAllEntries
    })
    return {entries}
}

const useEntryMutation = () => {
    const queryClient= useQueryClient()
    const newCourse = useMutation({
        mutationFn: ({newEntry} : {newEntry: NewEntry}) => createAnEntry({newEntry}),
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["entries"]})
        }
    })
    return {newCourse};

}


export {useAEntry, useGetAllEntries, useEntryMutation}



// --- Helper functions ---

async function fetchAnEntry(id: string){
    const response = await fetchWithAuth(
            `/notes/entries/${id}/`,
            {
                method: "GET",
            }
        );

    if(!response.ok){
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${response.status})`)
    }
    return response.json()

}


async function fetchAllEntries() {
    const response = await fetchWithAuth(
        `/notes/entries/`,
        {
            method: "GET",
        }
    );
    if(!response.ok){
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${response.status})`)
     }
    return response.json()
}


async function createAnEntry({newEntry}:{newEntry : NewEntry} ) {
    const response = await fetchWithAuth(
        '/notes/entries/',
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newEntry),
        }
    );
    if(!response.ok){
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${response.status})`)
     }
    return response.json()
}