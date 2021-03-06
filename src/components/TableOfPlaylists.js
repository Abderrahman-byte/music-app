import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { PlaylistRow } from './PlaylistRow'

import '../styles/TableOfPlaylists.scss'

export class TableOfPlaylists extends Component {
    render = () => {
        return (
            <table className='TableOfPlaylists'>
                <thead>
                    <tr>
                        <th className='text-start'>#</th>
                        <th>Playlist</th>
                        {this.props.withAuthor ? (
                            <th>Author</th>
                        ) : (null)}

                        <th>Tracks</th>
                        <th>Created Date</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {this.props.data?.map(playlist => <PlaylistRow 
                        deletePlaylist={this.props.deletePlaylist}
                        key={playlist.id} 
                        withAuthor={this.props.withAuthor} 
                        data={playlist}
                        updatePlaylist={this.props.updatePlaylist}
                    />)}
                </tbody>
            </table>
        )
    }
}

TableOfPlaylists.propTypes = {
    data: PropTypes.array.isRequired,
    withAuthor: PropTypes.bool,
    deletePlaylist: PropTypes.func.isRequired,
    updatePlaylist: PropTypes.func.isRequired
}

TableOfPlaylists.defaultProps = {
}