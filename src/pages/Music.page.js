import React from 'react'

import { ModelsContext } from '../context/ModelsContext'
import { PageHeader } from '../components/PageHeader'
import { LoadingModel } from '../components/LoadingModel'
import { TracksCardsContainer } from '../components/TracksCardsContainer'

export class MusicPage extends React.Component {
    static contextType = ModelsContext

    state = {
        data: [],
        currentPage: 1,
        itemsPerPage: 24,
        isLoading: true,
        nextRequestUrl: null
    }

    componentDidMount = () => {
        this.fetchMusicData()
    }

    fetchMusicData = async (withModel = true) => {
        const { openModel, closeModel } = this.context
        this.setState({...this.state, isLoading: true})
        if(withModel) openModel(<LoadingModel msg='Loading music data' />, false)

        let response = {data: []}
        const index = (this.state.currentPage - 1) * this.state.itemsPerPage
        const url = this.state.nextRequestUrl || `${process.env.API_URL}/api/music/tracks/top?index=${index}&limit=${this.state.itemsPerPage}`
        const req = await fetch(url)

        if(req.status >= 200 && req.status < 300) {
            response = await req.json()
        } else {
            console.error(await req.json())
        }

        this.setState((prevState) => {
            return {
                ...prevState,
                isLoading: false,
                currentPage: prevState.currentPage + 1,
                nextRequestUrl: response.next || null,
                data : [...prevState.data, ...response.data]
            }   
        })
        closeModel()
    }

    render = () => {
        return (
            <div className='MusicPage page'>
                <PageHeader title='Explore The Music' />
                <TracksCardsContainer data={this.state.data} />
                {!this.state.isLoading ? (
                    <div className='center-div'>
                        <button onClick={() => this.fetchMusicData(false)} className='btn-more'>load more</button>
                    </div>
                ) : (
                    <div className='center-div'>
                        <div className='lds-ring'>
                            <div></div>
                            <div></div>
                            <div></div>
                            <div></div>
                        </div>
                    </div>
                )}
            </div>
        )
    }
}