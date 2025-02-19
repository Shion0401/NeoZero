import React, { useEffect, useState ,useCallback} from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './top.module.css';
import fontstyles from '../font/font.module.css';
import pawloverslogoImg from './pawlovers.png';
import TopleftImg from '../image/Topleft.png';
import ToprightImg from '../image/Topright.png';
// import Cookies from 'js-cookie';

const TopPage = () => {
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  };

  const userid = getCookie('userid');
  const handlePost = () => {
    console.log(userid); // ここでuserIdが正しく取得できているかを確認
    navigate('/post',{state:{ userid } });
  };


  // 以下いいね用の関数
  const fetchGoodStatus = useCallback(async (postId) => {
    if (!userid || !postId) return 1;

    try {
      const response = await fetch(`https://neozero.metifie.com/post/goodstatus/${userid}/${postId}`);
      if (!response.ok) {
        throw new Error('※いいね状態の取得に失敗したニャン。');
      }

      const status = await response.json();
      return status;
    } catch (error) {
      console.error('※いいね状態取得エラー:', error);
      return 1;
    }
  }, [userid]);

  const handleGood = useCallback(async (postId) => { 
    if (!userid || !postId) return;

    try {
      const response = await fetch('https://neozero.metifie.com/post/good', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userid, postid: postId }),
      });

      if (!response.ok) {
        throw new Error('※いいねの更新に失敗したニャン。');
      }

      // window.location.reload();
      // 現在の投稿のいいね状態を反転させる（0 → 1 または 1 → 0）
      setPosts((prevPosts) => {
        return prevPosts.map((post) => {
          if (post.post_id === postId) {
            return {
              ...post,
              isLiked: post.isLiked === 1 ? 0 : 1,  // 1 → 0, 0 → 1
            };
          }
          return post;
        });
      });

    } catch (error) {
      console.error('※いいね処理エラー:', error);
    }
  }, [userid]);

  // 以下フォロー用の関数
  const fetchFollowStatus = useCallback(async (postId) => {
    if (!userid || !postId) return 1;

    try {
      const response = await fetch(`https://neozero.metifie.com/post/followstatus/${userid}/${postId}`);

      if (!response.ok) {
        throw new Error('※フォロー状態の取得に失敗したニャン。');
      }

      const status = await response.json();
      return status;
    } catch (error) {
      console.error('※フォロー状態取得エラー:', error);
      return 1;
    }
  }, [userid]);

  const handleFollow = useCallback(async (followedid) => {
    if (!userid || !followedid) return;

    try {
      const response = await fetch('https://neozero.metifie.com/follow', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userid, followedid }),
        
      });

      if (!response.ok) {
        throw new Error('※フォローの更新に失敗したニャン。');
      }

      // window.location.reload();
      // フォロー状態の反転処理
      setPosts((prevPosts) => {
        return prevPosts.map((post) => {

          // 同じユーザーが投稿した他の投稿にも反映
          if (post.user_id === followedid) {
            return {
              ...post,
              isFollowed: post.isFollowed === 0 ? 1 : 0, // フォロー状態を反転
            };
          }

          return post;
        });
      });

    } catch (error) {
      console.error('フォロー処理エラー:', error);
    }
  }, [userid]);



  const handleMypage = () => {
    navigate('/mypage');
  };


  const handleReport = (postId) => {
    navigate(`/report_con`, { state: { postId } });
  }

  const handlesuperchat = () => {
    //外部サイトへ飛ぶ(新しいタブで)
    //window.open('https://buy.stripe.com/test_6oEdQVahC6wN5Ko5kn', '_blank', 'noopener noreferrer')
  };

  const inputStyle = {
    fontFamily: 'CraftMincho, serif',
  };
//広告ボタン
  const handlead1 = () => {
    //外部サイトへ飛ぶ(新しいタブで)
    //window.open('https://www.info.kochi-tech.ac.jp/faculty_members/profile_shinomori.shtml', '_blank', 'noopener noreferrer')
    window.open('https://anisupo.jimdofree.com/', '_blank', 'noopener noreferrer')
  };

  const handlead2 = () => {
    //外部サイトへ飛ぶ(新しいタブで)
    //window.open('https://www.info.kochi-tech.ac.jp/faculty_members/profile_iwata.shtml', '_blank', 'noopener noreferrer')
    window.open('https://anisupo.jimdofree.com/', '_blank', 'noopener noreferrer')
  };
  useEffect(() => {
    const fetchPosts = async () => {
      if (!userid) {
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        const response = await fetch('https://neozero.metifie.com/post/new');
        if (!response.ok) {
          throw new Error('※投稿の取得に失敗したニャン。');
        }
        const data = await response.json();
        console.log(posts.image)
        const postsWithStatuses = await Promise.all(
          data.map(async (post) => {
            const goodStatus = await fetchGoodStatus(post.post_id);
            const followStatus = await fetchFollowStatus(post.post_id);
            return {
              ...post,
              isLiked: goodStatus,
              isFollowed: followStatus
            };
          })
        );

        setPosts(postsWithStatuses);
      } catch (error) {
        console.error('Error fetching posts:', error);
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, [userid]);
  // }, [userid, fetchGoodStatus, fetchFollowStatus]); // 依存配列にfetchGoodStatusとfetchFollowStatusを追加

  if (isLoading) {
    return <div className={styles.loading}>読み込み中...</div>;
  }

  if (error) {
    return <div className={styles.error}>エラー: {error}</div>;
  }

  return (
    <div className={fontstyles.fontFamily}>
      <div className={styles.body}>
        <div className={styles.above}>
          <img
            src={pawloverslogoImg}
            alt="PawLovers"
            className={styles.pawloverslogoImg}
          />

          <button
            className={styles.postButton}
            onClick={handlePost}
            style={inputStyle}
          >
            投稿する
          </button>

          <button
            className={styles.mypageButton}
            onClick={handleMypage}
            style={inputStyle}
          >
            マイページ
          </button>
        </div>

        <div className={styles.bottom}>
          <div className={styles.advertisement}>
          <button
            className={styles.adbutton}
              onClick={handlead1}
            >
            <img
              src={TopleftImg}
              alt="広告"
            />
            </button>
          </div>

          <div className={styles.media}>
            {posts.map((post) => (
              <div key={post.post_id} className={styles.white}>
                <div className={styles.post}>
                  <div className={styles.picture}>
                    <img
                      // alt ={`${post.postimag}`} // 修正された部分
                      //alt={`投稿 ${post.image}`}
                      // className={styles.postImage}
                      src={post.image} 
                      onError={(e) => {
                        e.target.src = '/placeholder.png';
                        console.error('※画像の読み込みに失敗したニャン。');
                      }}
                    />
                  </div>

                  <div className={styles.info}>
                   {post.user_id !== userid && (
                    <button
                      className={styles.followButton}
                      onClick={() => handleFollow(post.user_id)}
                      style={inputStyle}
                    >
                      {post.isFollowed ? 'フォロー中' : 'フォロー'}
                    </button>
                      )
                    }

                    <div className={styles.push}>
                      <button
                        className={styles.good}
                        onClick={() => handleGood(post.post_id)} //post.idを取得
                        style={inputStyle}
                      >
                        {post.isLiked ? 'いいね済み' : 'いいね'}
                      </button>

                      <button
                        className={styles.good}
                        onClick={handlesuperchat}
                        style={inputStyle}
                      >
                        スパチャ
                      </button>
                    </div>

                    <div className={styles.comment}>
                      <b>{post.name}ちゃん<br></br></b>
                      <br></br>
                      <b>「{post.title}わん」<br></br></b>
                      <br></br>
                      {post.comment}ニャン
                    </div>
                    <button
                      className={styles.reportButton}
                      onClick={() => handleReport(post.post_id)}
                      style={inputStyle}
                    >
                      通報
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className={styles.advertisement}>
            <button
            className={styles.adbutton}
              onClick={handlead2}
            >
              <img
                src={ToprightImg}
                alt="広告"
              />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopPage;
