export const useRagApi = () => {
  // Use config or default to localhost:8000
  const API_BASE = 'http://localhost:8000';

  const chat = async (message, collectionName="default") => {
    try {
      const data = await $fetch(`${API_BASE}/api/v1/chat/chat`, {
        method: 'POST',
        body: { 
          "question": message,
          "collection_name": collectionName
         } 
      });
      return data;
    } catch (err) {
      console.error('Chat API Error:', err);
      throw err;
    }
  };

  const ingest = async (selectedFiles, collectionName="default") => {
    console.log(selectedFiles);
    const formData = new FormData();

    const selectedFilesArray = Array.isArray(selectedFiles) 
    ? selectedFiles
    : [selectedFiles];

    console.log(selectedFilesArray);

    selectedFilesArray.forEach(file =>{
      console.log("name",file);
      formData.append('files', file);
    })

    formData.append("collection_name", collectionName)
    console.log(formData);

    try {
      const data = await $fetch(`${API_BASE}/api/v1/ingest/upload`, {
        method: 'POST',
        body: formData,
      });
      return data;
    } catch (err) {
      console.error('Ingest API Error:', err);
      throw err;
    }
  };

  return {
    chat,
    ingest
  };
};
