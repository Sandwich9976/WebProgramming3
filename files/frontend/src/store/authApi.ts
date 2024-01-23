import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

// Define a service using a base URL and expected endpoints
export const authApi = createApi({
  reducerPath: 'authApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/' }),
  endpoints: (builder) => ({
    getToken: builder.mutation<{"access_token": string; "token_type": "Bearer"; user_id: number}, FormData>({
      query: (formData) => {
        return{
            url: "/api/get-token",
            method: "POST",
            body: formData
        }
    },
    }),
  }),
})

export const {useGetTokenMutation} = authApi