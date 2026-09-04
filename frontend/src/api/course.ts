import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { fetchWithAuth } from "./fetchWithAuth";
import { Course, NewCourse } from "../types/types";



const useACourse =(id?: string | null)=> {
    
    
    const course = useQuery({
        queryKey: ["aCourse", id],
        queryFn: () => fetchACourse(id!),
    });

    return {course}
}


const useGetAllCourses = () => {
      const courses = useQuery({
        queryKey: ["courses"],
        queryFn: fetchCourses
    });

    return {courses}
}

const useCourseMutation = () =>{
    const queryClient= useQueryClient()
    const courseMutation = useMutation({
            mutationFn: async ({
                    newCourse 
                } : {
                    newCourse : NewCourse
            }) => {
                return await createCourse(newCourse)
            },
            onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["courses"]})
        }
        }) 
    
    return {courseMutation}
}

export {useACourse, useGetAllCourses, useCourseMutation}
// --- Helper function ---

async function fetchACourse(id: string): Promise<Course | null> {
    const response = await fetchWithAuth(
        `/courses/${id}/`,
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

async function fetchCourses(): Promise<Response> {
    const response = await fetchWithAuth(
        "/courses/",
        {
            method: "GET"
        }
    );
     if(!response.ok){
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${response.status})`)
    }
    return response.json();
}

async function createCourse(newCourse: NewCourse ): Promise<Response> {
    const response = await fetchWithAuth(
        "/courses/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newCourse),
        },
    );
    if(!response.ok){
        const data = await response.json().catch(() => null)
        throw new Error(data?.detail || `Request failed (${response.status})`)
    }
    return response.json()
}