import React, { createContext, useCallback, useState } from 'react'

export const ModelsContext = createContext({})
ModelsContext.displayName = 'ModelsContext'

export const ModelsProvider = ({children}) => {
    const [isOpen, setOpenStatus] = useState(false)
    const [model, setModel] = useState(null)
    const [isClosable, setClosableState] = useState(false)

    const openModel = (model, isClosable = false) => {
        setModel(model)
        setOpenStatus(true)
        setClosableState(isClosable)
    }

    const closeModel = () => {
        setModel(null)
        setOpenStatus(false)
        setClosableState(false)
    }
    
    const backdropClickEvent = useCallback(() => {
        if(isClosable) {
            closeModel()
        }
    }, [isClosable])

    return (
        <ModelsContext.Provider value={{openModel, closeModel, isOpen, model, backdropClickEvent}}>
            {children}
        </ModelsContext.Provider>
    )
}