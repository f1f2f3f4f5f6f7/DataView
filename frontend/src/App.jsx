import { useRef, useState } from 'react'
import { Toast } from 'primereact/toast'
import { FileUpload } from 'primereact/fileupload'
import { ProgressBar } from 'primereact/progressbar'
import { Button } from 'primereact/button'
import { Tooltip } from 'primereact/tooltip'
import { Tag } from 'primereact/tag'
import './App.css'

export default function App() {
  const toast = useRef(null)
  const fileUploadRef = useRef(null)
  const [totalSize, setTotalSize] = useState(0)
  const [darkMode, setDarkMode] = useState(false)

  const toggleTheme = () => {
    const theme = darkMode ? 'lara-light-blue' : 'lara-dark-blue'
    const link = document.getElementById('theme-link')
    link.href = `/node_modules/primereact/resources/themes/${theme}/theme.css`
    setDarkMode(!darkMode)
  }

  const triggerFileSelect = () => {
    const inputs = document.querySelectorAll('input[type="file"]')
    if (inputs.length > 0) inputs[0].click()
  }

  const onTemplateSelect = (e) => {
    let _totalSize = totalSize
    Object.keys(e.files).forEach((key) => { _totalSize += e.files[key].size || 0 })
    setTotalSize(_totalSize)
  }

  const onTemplateUpload = (e) => {
    let _totalSize = 0
    e.files.forEach((file) => { _totalSize += file.size || 0 })
    setTotalSize(_totalSize)
    toast.current.show({ severity: 'info', summary: 'Success', detail: 'File Uploaded' })
  }

  const onTemplateRemove = (file, callback) => {
    setTotalSize(totalSize - file.size)
    callback()
  }

  const onTemplateClear = () => setTotalSize(0)

  const headerTemplate = (options) => {
  const { className, chooseButton, cancelButton } = options
  const value = totalSize / 10000
  const formatedValue = fileUploadRef && fileUploadRef.current
    ? fileUploadRef.current.formatSize(totalSize)
    : '0 B'
  const isNearLimit = value >= 80

  return (
    <div className={className} style={{ backgroundColor: 'transparent', display: 'flex', alignItems: 'center', minHeight: '58px' }}>
      <div style={{ opacity: totalSize > 0 ? 1 : 0, pointerEvents: totalSize > 0 ? 'auto' : 'none', width: '42px' }}>
        {chooseButton}
      </div>
      {cancelButton}
      <div className="flex align-items-center gap-3 ml-auto">
        <span style={{ color: isNearLimit ? '#ef4444' : 'inherit' }}>{formatedValue} / 500 MB</span>
        <ProgressBar value={value} showValue={false}
          style={{ width: '10rem', height: '12px' }}
          color={isNearLimit ? '#ef4444' : '#38bdf8'} />
      </div>
    </div>
  )
}

  const itemTemplate = (file, props) => (
    <div className="gallery-item">
      <img alt={file.name} role="presentation" src={file.objectURL} />
      <div className="gallery-item-info">
        <span className="gallery-item-name">{file.name}</span>
        <small>{new Date().toLocaleDateString()}</small>
        <div className="gallery-item-footer">
          <Tag value={props.formatSize} severity="warning" />
          <Button type="button" icon="pi pi-times"
            className="p-button-outlined p-button-rounded p-button-danger"
            onClick={() => onTemplateRemove(file, props.onRemove)} />
        </div>
      </div>
    </div>
  )

  const emptyTemplate = () => (
    <div className="empty-drop-area" onClick={triggerFileSelect}>
      <i className="pi pi-image" />
      <span>Arrastra tus archivos aquí o haz clic para seleccionar</span>
    </div>
  )

  const chooseOptions = {
    icon: 'pi pi-fw pi-images',
    iconOnly: true,
    className: 'custom-choose-btn p-button-rounded p-button-outlined',
  }
  const uploadOptions = { style: { display: 'none' } }
  const cancelOptions = { style: { display: 'none' } }

  return (
    <div className="page">
      <Toast ref={toast} />
      <Tooltip target=".custom-choose-btn" content="Agregar más" position="bottom" />

      <button className="theme-toggle" onClick={toggleTheme}>
        <i className={`pi ${darkMode ? 'pi-sun' : 'pi-moon'}`} />
      </button>

      <h1 className="title">DataView</h1>

      <div className="upload-wrapper">
        <FileUpload
          ref={fileUploadRef}
          name="file"
          url="/api/upload"
          multiple
          accept="image/*"
          maxFileSize={500000000}
          onUpload={onTemplateUpload}
          onSelect={onTemplateSelect}
          onError={onTemplateClear}
          onClear={onTemplateClear}
          headerTemplate={headerTemplate}
          itemTemplate={itemTemplate}
          emptyTemplate={emptyTemplate}
          chooseOptions={chooseOptions}
          uploadOptions={uploadOptions}
          cancelOptions={cancelOptions}
        />
      </div>

      <div className="action-buttons">
        <Button
          label="Cargar"
          onClick={() => fileUploadRef.current.upload()}
          disabled={totalSize === 0}
        />
        <Button
          label="Limpiar"
          className="p-button-outlined p-button-secondary"
          onClick={() => fileUploadRef.current.clear()}
          disabled={totalSize === 0}
        />
      </div>
    </div>
  )
}