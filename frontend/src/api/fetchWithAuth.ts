import Cookies from 'js-cookie'

/// Get CSRF token to send only when unsafe method is used 


export async function fetchWithAuth(url: string, options: RequestInit = {}) {
    const cookie: string | undefined = Cookies.get("csrftoken");
    if (!cookie) throw new Error("No CSRF token — is the session set up?");
    const safeMethods = ["GET", "HEAD", "OPTIONS"];
    const method = (options.method || "GET").toUpperCase();
    const headers: Record<string, string> = { ...(options.headers as Record<string, string>) };    
    if (!safeMethods.includes(method)) {
        headers["X-CSRFToken"] = cookie
    }
    const res = await fetch(url, {
        ...options,
        headers
        
    });
    return res
}