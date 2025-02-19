import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './nyakama.module.css';
import fontstyles from '../font/font.module.css';
import Left1Img from '../image/Left1.png';
import Right1Img from '../image/Right1.png';
import Icondog from './icon/3.png';
import Iconcat from './icon/4.png';

const Nyakama = () => {
  const navigate = useNavigate();
  const [followlists, setFollows] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleTop = () => {
    navigate('/top');
  };

  const handleUser = (followedid) => {
    navigate(`/other_users/${followedid}`);
  };

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  };
  const userid = getCookie('userid');

  const handleReFollow = useCallback(async (followedid) => {
    console.log(followedid)
      if (!userid || !followedid) return;

      console.log(followedid)
    
      try {
        const response = await fetch('https://neozero.metifie.com/follow', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userid, followedid }),
        });

        if (!response.ok) {
          throw new Error('※フォローの更新に失敗したワン。');
        }
        const status = await response.json();
        // console.log(status);

        window.location.reload();

      } catch (error) {
        console.error('フォロー処理エラー:', error);
      }
    }, [userid]);

  const inputStyle = {
    fontFamily: 'CraftMincho, serif'
  };

  useEffect(() => {
    const fetchFollowList = async (userid) => {
      if (!userid) {
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        const response = await fetch(`https://neozero.metifie.com/followlist/${userid}`);
        if (!response.ok) {
          throw new Error('※フォローリストの取得に失敗したワン');
        }
        const followListData = await response.json();
        console.log('followListData',followListData);
        setFollows(followListData);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchFollowList(userid);
  }, [userid, handleReFollow]);

  if (isLoading) {
    return <div className={styles.loading}>読み込み中...</div>;
  }


  if (error) {
    return <div className={styles.error}>エラー: {error}</div>;
  }

  const handlead1 = () => {
    //外部サイトへ飛ぶ(新しいタブで)
    //window.open('https://www.info.kochi-tech.ac.jp/faculty_members/profile_matsuzaki.shtml', '_blank', 'noopener noreferrer')
    window.open('https://anisupo.jimdofree.com/', '_blank', 'noopener noreferrer')
  };

  const handlead2 = () => {
    //外部サイトへ飛ぶ(新しいタブで)
    //window.open('https://www.info.kochi-tech.ac.jp/faculty_members/profile_takata.shtml', '_blank', 'noopener noreferrer')
    window.open('https://anisupo.jimdofree.com/', '_blank', 'noopener noreferrer')
  };

  return (
    <div className={fontstyles.fontFamily}>
      <div className={styles.body}>
        <div className={styles.left}>
          <button
            className={styles.topButton}
            onClick={handleTop}
            style={inputStyle}
          >
            トップページへ戻る
          </button>
          <div className={styles.advertisement}>
            <button
              className={styles.adbutton}
              onClick={handlead1}
            >
              <img
                src={Left1Img}
                alt="Left1Img"
              />
            </button>
          </div>
        </div>
        <div className={styles.center}>
          <div className={styles.title}>Nyakama</div>
          <div className={styles.media}>
            {followlists.map((follow) => (
              <div key={follow.id} className={styles.white}>
                <div className={styles.photo}>
                  <img
                    src={Iconcat}
                    alt="cat_icon"
                  /></div>
                <div className={styles.info}>
                  <div className={styles.detail}>
                    <button
                      className={styles.name}
                      onClick={() => handleUser(follow.id)}
                      style={inputStyle}
                    >
                      {follow.name}
                    </button>
                    <button
                    className={styles.refollowButton}
                    onClick={() => {
                      console.log('フォロー解除',follow.follwedid);  // follow.id が正しく表示されるか確認
                      handleReFollow(follow.follwedid);
                    }}
                    style={inputStyle}
                  >
                      フォロー解除
                    </button>
                  </div>
                  <div className={styles.comment}>{follow.comment}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className={styles.right}>
          <div className={styles.advertisement2}>
            <button
              className={styles.adbutton}
              onClick={handlead2}
            >
              <img
                src={Right1Img}
                alt="Right1Img"
              />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Nyakama;
