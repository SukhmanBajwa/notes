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
        "/api/me/",
        {
            method: "GET",
        },
    );
    if (response.ok) return response.json();
    return null;
    
}

async function login(email: string, password: string): Promise<Response> {
    const response = await fetchWithAuth(
        "/api/login/",
        {
            method: "POST",
            
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        },
    );
    if (!response.ok){
        throw Error(`HTTP error! Status: ${response.status}`)
    }
    return response;
}

async function logout(){
    const _response = await fetchWithAuth(
        "/api/logout/",
        {
            method: "POST",
        }
    );
    if (!_response.ok){
        throw Error(`HTTP error! Status: ${_response.status}`)
    } 
}
