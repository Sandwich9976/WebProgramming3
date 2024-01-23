import { createApi } from '@reduxjs/toolkit/query/react'
import { baseQueryWithAuth } from "./baseQueryWithAuth"


export const reviewApi = createApi({
    reducerPath: 'review',
    baseQuery: baseQueryWithAuth,
    endpoints: (builder) => ({
      createReview: builder.mutation<{
        "review_text": string,
        "review_id": number,
        "user_id": number
      },{reviewText: string, userId: number|null}>({
        query: ({userId, reviewText}) => {
          return{
              url: "/api/review",
              method: "POST",
              body: {review_text: "reviewText", user_id: (userId ?? "").toString()}
          }
      },
      }),
    }),
  })

export const {useCreateReviewMutation} = reviewApi  