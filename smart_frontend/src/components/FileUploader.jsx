/**
 * FileUploader Component
 * Componente minimalista para carga de archivos .txt de mapas
 */

import { useState } from 'react';
import { useMap } from '../context';
import './FileUploader.css';

const FileUploader = () => {
  const { uploadMap, resetMap, loading, error, clearError } = useMap();
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (file) => {
    if (file) {
      if (!file.name.endsWith('.txt')) {
        alert('Solo se permiten archivos .txt');
        return;
      }
      setSelectedFile(file);
      clearError();
    }
  };

  const handleInputChange = (event) => {
    handleFileChange(event.target.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileChange(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      await uploadMap(selectedFile);
      setSelectedFile(null);
    } catch (err) {
      console.error('Error uploading map:', err);
    }
  };

  const handleReset = async () => {
    try {
      await resetMap();
      setSelectedFile(null);
    } catch (err) {
      console.error('Error resetting map:', err);
    }
  };

  return (
    <div className="file-uploader">
      <h3 className="uploader-title">Cargar Mapa Marciano</h3>
      
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".txt"
          onChange={handleInputChange}
          disabled={loading}
          id="file-input"
          className="file-input-hidden"
        />
        <label htmlFor="file-input" className="drop-zone-label">
          {selectedFile ? (
            <>
              <span className="file-icon">📄</span>
              <span className="file-name">{selectedFile.name}</span>
            </>
          ) : (
            <>
              <span className="upload-icon">📁</span>
              <p className="drop-text">Arrastra un archivo .txt aquí</p>
              <p className="or-text">o</p>
              <span className="browse-btn">Seleccionar archivo</span>
            </>
          )}
        </label>
      </div>

      {error && (
        <div className="error-banner">
          <span className="error-icon">⚠️</span>
          <span className="error-text">{error}</span>
          <button onClick={clearError} className="error-close">✕</button>
        </div>
      )}

      <div className="uploader-actions">
        <button
          onClick={handleUpload}
          disabled={!selectedFile || loading}
          className="btn btn-primary"
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Cargando...
            </>
          ) : (
            <>
              <span>🚀</span>
              Cargar Mapa
            </>
          )}
        </button>

        <button
          onClick={handleReset}
          disabled={loading}
          className="btn btn-secondary"
        >
          <span>🔄</span>
          Reiniciar
        </button>
      </div>
    </div>
  );
};

export default FileUploader;
