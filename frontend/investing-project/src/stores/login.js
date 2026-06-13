import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State (using Composition API)
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(false)

  // Actions
  async function login(username, password) {
    try {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password',password)
      const response = await axios.post("http://127.0.0.1:8000/api/user/token", 
      formData)

      token.value = response.data.access_token  // Using .value
      user.value = response.data.user
      isAuthenticated.value = true
      localStorage.setItem('token', response.data.access_token)
    } catch (error) {
      throw error
    }
  }

  function logout() {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
  }

  async function checkAuth() {
    if (token.value) {
      isAuthenticated.value = true
    }
  }

  return { user, token, isAuthenticated, login, logout, checkAuth }
})
