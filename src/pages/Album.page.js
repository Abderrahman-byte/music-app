import React from 'react'

import { LoadingModel } from '../components/LoadingModel'
import { PlaylistHeader } from '../components/PlaylistHeader'
import { ModelsContext } from '../context/ModelsContext'
import { PlaylistTable } from '../components/PlaylistTable'
import { AlbumNotFound } from '../components/NotFound'

export class AlbumPage extends React.Component {
    static contextType = ModelsContext

    state = {
        data: null,
        isLoading: true,
        items: [],
        error: false
    }

    componentDidMount = () => {
        this.fetchAlbumData()
    }

    fetchAlbumData = async () => {
        const { openModel, closeModel } = this.context
        openModel(<LoadingModel msg='Loading Album data' />, false)

        const id = this.props?.match?.params?.id
        const req = await fetch(`${process.env.API_URL}/api/music/album/${id}`)

        if(req.status >= 200 && req.status < 300) {
            const data = await req.json()
            const items = data.tracks || []
            const newState = { data, items, isLoading: false , error: false}
            this.setState({...this.state, ...newState})
        } else {
            console.log(await req.json())
            this.setState({...this.state, error: true})
        }
        closeModel()
    }

    getHeaderData = () => {
        return {
            cover: this.state.data?.cover_medium,
            title: this.state.data?.title,
            itemsNb: this.state.data?.nb_tracks,
            release_date: this.state.data?.release_date,
            author: {
                id: this.state.data?.artist?.id,
                name: this.state.data?.artist?.name,
                picture: this.state.data?.artist?.picture_small,
            },
            items: this.state.items,
            autoPlay: this.props.location?.state?.autoPlay || false
        }
    }

    render = () => {
        if(this.state.error) {
            return (
                <div className='AlbumPage page'>
                    <AlbumNotFound />
                </div>
            )
        } else {
            return (
                <div className='AlbumPage page'>
                    {this.state.isLoading ? (null) : (
                        <>
                        <PlaylistHeader {...this.getHeaderData()}/>
                        <PlaylistTable items={this.state.items}/>
                        </>
                    )} 
                </div>
            )
        }
    }
}