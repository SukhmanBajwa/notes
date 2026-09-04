import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { fetchWithAuth } from "./fetchWithAuth";
import { Course, CreatingCourse } from "../types/types";



const useCourse =(id?: string | null)=> {
    const queryClient= useQueryClient()
    
    const course = useQuery({
        queryKey: ["aCourse", id],
        queryFn: () => fetchACourse(id!),
        enabled: !!id,
    });

    const courses = useQuery({
        queryKey: ["courses"],
        queryFn: fetchCourses
    });

    const courseMutation = useMutation({
        mutationFn: async ({
                newCourse 
            } : {
                newCourse : CreatingCourse
        }) => {
            return await createCourse(newCourse)
        }
    }) 

    return {course, courses, courseMutation}
}
export {useCourse}

// --- Helper function ---

async function fetchACourse(id: string): Promise<Course | null> {
    const response = await fetchWithAuth(
        `/api/v1/courses/${id}/`,
        {
            method: "GET",

        },
    );
    if (!response.ok){
        throw new Error(`HTTP error! Status: ${response.status}`)
    }
    return response.json();
}

async function fetchCourses(): Promise<Response> {
    const response = await fetchWithAuth(
        "/api/v1/courses/",
        {
            method: "GET"
        }
    );
    if (!response.ok){
        throw new Error(`HTTP error! Status: ${response.status}`)
    }
    return response.json();
}

async function createCourse(newCourse: CreatingCourse ): Promise<Response> {
    const response = await fetchWithAuth(
        "/api/v1/courses/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({...newCourse}),
        },
    );
    if (!response.ok){
        throw new Error(`HTTP error! Status: ${response.status}`)
    }
    return response.json()
}