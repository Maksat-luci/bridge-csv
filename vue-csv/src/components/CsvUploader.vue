<template>
  <div>
    <h1>Upload CSV File</h1>
    <input type="file" @change="handleFileUpload" accept=".csv">
    <button v-if="file" @click="submitFile">Submit</button>
    <div v-if="file">
      <p>File Name: {{ file.name }}</p>
      <p>File Size: {{ fileSize }}</p>
    </div>
    <div v-if="error">
      <p>Error: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      file: null,
      error: null
    }
  },
  computed: {
    fileSize() {
      if (!this.file) return ''
      const size = Math.round(this.file.size / 1024)
      return `${size} KB`
    }
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0]
      this.error = null
    },
    async submitFile() {
      try {
        const formData = new FormData()
        formData.append('csv', this.file)
        await axios.post('http://parsecsv.duckdns.org/uploadcsv', formData)
        alert('File successfully uploaded!')
        alert(formData)
        console.info(formData)
      } catch (err) {
        console.error(err)
        this.error = err.message
      }
    }
  }
}
</script>

<style>
h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

input[type="file"] {
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #388e3c;
}

p {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.error {
  color: red;
  font-weight: bold;
}
</style>
