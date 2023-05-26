<template>
  <div>
    <form>
      <div class="form-group">
        <label for="csvFile">Выберите файл:</label>
        <input type="file" id="csvFile" @change="csvFile = $event.target.files[0]">
            </div>
      <button type="button" class="btn btn-primary" @click="uploadCsv">Отправить</button>
    </form>
    <div>{{ responseMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
    responseMessage: '',
    };
  },
  methods: {
    uploadCsv() {
      const formData = new FormData();
      formData.append("csv", this.csvFile, this.csvFile.name);
      axios.post("http://localhost:8000/updatecsv", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      .then(response => {
         this.responseMessage = response.data;
      })
      .catch(error => {
        this.responseMessage = error;
      });
    }
  }
}
</script>
