export const state = () => ({
    images: []
  })
  
  export const getters = {
    getImages(state) {
        return state.images
    }
  }
  
  export const mutations = {
    push(state, data) {
        state.images.push({
            image: data.image,
            url: data.url,
            predict: data.predict
        })
    }
  }
  
  export const actions = {
  
  }