// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    ip:{},
    ipextra:{}
  }),
  getters:{
    getCheck: state => ip => state.ipextra[ip].check
  },
  mutations:{
    setCheck(e) {
      this.ipextra[e]['check'] = !this.ipextra[e]['check']
    }
  },
  actions:{
    async getIp() {
      try {
        const res = await fetch("http://localhost:3001/data")
        const data = await res.json();
        this.ip = data;
        this.ipextra = Object.fromEntries(Object.keys(data).map(ipAddress => [ipAddress, {
          "check":false,
          "comments":null
        }]));
      } catch(e) {
        console.log(e)
      }
    }
  }
})
