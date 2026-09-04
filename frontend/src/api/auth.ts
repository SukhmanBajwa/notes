import { useQuery, useMutation, useQueryClient} from "@tanstack/react-query"
import { fetchWithAuth } from "./fetchWithAuth"
import { UserData } from "../types/types";
// import { useNavigate } from "react-router";


const useUserData = () => {
    const userData = useQuery({
        queryKey: ["me"],
        queryFn: fetchUser
    });
    return {userData}
}
export {useUserData};

const useAuth = () => {
    const queryClient = useQueryClient();
    // const navigate = useNavigate();

    const loginMutation = useMutation({
        mutationFn: async ({
            email,
            password,
        }: {
            email: string;
            password: string;
        }) => {
            return await login(email, password);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["me"]})
        }
    })
    

    const logoutMutation = useMutation({
        mutationFn: async () => {
            return await logout();
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["me"]})
        }
    })       
    
    return {
        loginMutation,
        logoutMutation,
    }
}
export {useAuth};

// --- Helper functions ---
async function fetchUser(): Promise<UserData | null> {
    const response = await fetchWithAuth(
        "/me/",
        {
            method: "GET",
        },
    );
    if(!response.ok){
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${response.status})`)
    }
    return response.json();
    
}

async function login(email: string, password: string): Promise<Response> {
    const response = await fetchWithAuth(
        "/login/",
        {
            method: "POST",
            
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        },
    );
    if(!response.ok){
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${response.status})`)
    }
    return response.json();
}

async function logout(){
    const _response = await fetchWithAuth(
        "/logout/",
        {
            method: "POST",
        }
    );
    if(!_response.ok){
        const data = await _response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${_response.status})`)
    }
    
}
