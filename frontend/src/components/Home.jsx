import {useQuery, gql} from '@apollo/client'


const GET_USERNAME = gql`
  query GetUsername {
    getUsername {
      username
    }
  }
`;

const Home = () => {
    const { loading: usernameLoading, error: usernameError, data: usernameData } = useQuery(GET_USERNAME);

    if ( usernameLoading) return <p>Loading...</p>;
    if ( usernameError) return <p>{ usernameError.message}</p>;

    const username = usernameData?.getUsername?.username;

    return (
        <div>
            <h1>Home</h1>
            <div>
                {username ? (
                    <>
                    <p>Hi, {username}</p>
                    </>
                ) : (
                    <button onClick={() => console.log('Redirect to login')}>Log in</button>
                )}
            </div>
        </div>
    );

};

export default Home